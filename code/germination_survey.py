#!/usr/bin/env python3

import datetime
import os
import shutil
import subprocess
import sys

import numpy as np
import pandas as pd

from common import days_after_planting, standardize_farm_id, unique_farm_id
import odkcentral as odk


def downloadFiles(form_url: str) -> pd.DataFrame:
    folder = odk.download_submissions(form_url)

    data1_path = folder/ "Cassava-SOS-Germination-Survey.csv"
    data2_path = folder / "Cassava-SOS-Germination-Survey-plot_survey.csv"

    # load data
    data1 = pd.read_csv(data1_path)
    data2 = pd.read_csv(data2_path)

    # merge data1 and data2 (i.e., the repeat or loop csv file)
    data1["PARENT_KEY"] = data1["KEY"]
    data3 = data2.merge(data1, on="PARENT_KEY")

    shutil.rmtree(folder)
    
    return data3 # return merged data, where each row is data for a plot


def addGerminationVersionInfo(data: pd.DataFrame) -> pd.DataFrame:
    def getVersion(DAP: int, county: str) -> int:
        county = county.lower()
        if county == "migori":
            if DAP <= 25:
                return 1
            return 2
        elif county in ["homabay", "busia", "baringo", "kilifi", "bungoma"]:
            if DAP <= 15:
                return 1
            return 2
        elif county == "siaya":
            if DAP <= 16:
                return 1
            return 2
        
    # load planing date information for all farms/ # change later
    try:
        planting_date = pd.read_csv("output/cassava_sos_planting_survey.csv")
    except:
        subprocess.run(["python3", "planting_survey.py"], check=True)
        planting_date = pd.read_csv("output/cassava_sos_planting_survey.csv")

    # standardize ID
    data["farm_id"] = data["farm_id"].apply(standardize_farm_id)
    planting_date["farm_id"] = planting_date["farm_id"].apply(standardize_farm_id)

    data = planting_date[["farm_id", "planting_date"]].merge(data, on="farm_id")

    # date format surveys 
    data["planting_date"] = pd.to_datetime(data["planting_date"])
    data["survey_date"] = pd.to_datetime(data["date"])

    # get Days after planting for which all the surveys were done
    data["DAP"] =\
        data.apply(lambda x: days_after_planting(x["survey_date"], x["planting_date"]), axis=1)

    # add survey version info
    data["survey_version"] = data.apply(lambda x: getVersion(x["DAP"], x["county"]), axis=1)

    return data


def preProcessData(data):
    data["farm_id"] =\
        data.apply(lambda x: unique_farm_id(x["county"], x["field_id"]), axis=1)

    # germination metrics
    data["germination_rate"] = data["germination_num"] / 36
    data["germination_percent"] = data["germination_rate"] * 100

    # add survey version info 
    data = addGerminationVersionInfo(data)

    # reduce the columns 
    filter_cols = [
        'block', 'plot', 'treatment', 'biochar_rate', 'cassav_variety',
        'germination_num', 'erosion', 'holes_affected_by_erosion',
        'termites', 'holes_affected', 'SubmissionDate', 'date', 'county',
        'field_id', 'location-Latitude', 'location-Longitude',
        'location-Altitude', 'location-Accuracy', 'farm_id',
        'survey_version', 'germination_percent'
    ]
    data = data[filter_cols]
    return data


def main():
    form_url = "https://opendatakit.plantvillage.psu.edu/v1/projects/265/forms/Cassava-SOS-Germination-Survey/"
    data = downloadFiles(form_url)
    processed_data = preProcessData(data)
    processed_data.to_csv("output/cassava_sos_germination_survey.csv", index=False)


if __name__ == "__main__":
    main()