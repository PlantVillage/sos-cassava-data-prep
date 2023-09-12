#!/usr/bin/env python3

import datetime
import os
import sys

import numpy as np
import pandas as pd

# import odkcentral
sys.path.insert(0, "module") # relative path to the module folder
import odkcentral as odk


# download odk central files
def downloadFiles(form_url):
    folder = odk.downloadSubmissions(form_url)

    # set path
    data1_path = f"{folder}/{os.listdir(folder)[0]}"
    data2_path = f"{folder}/{os.listdir(folder)[1]}"

    # load data
    data2 = pd.read_csv(data1_path); data1 = pd.read_csv(data2_path)

    # remove rejected and has issues surveys
    data1 = data1[data1["ReviewState"] != 'rejected']
    data1 = data1[data1["ReviewState"] != 'hasIssues'] 

    # merge data1 and data2 (i.e., the repeat or loop csv file)
    data1["PARENT_KEY"] = data1["KEY"]
    data3 =  data2.merge(data1, on="PARENT_KEY")

    return data3 # return merged data, where each row is data for a plot

def addGerminationVersionInfo(data):
    
    def standardizeFarmID(farm_id):
        return farm_id.lower()
    
    def getDAP(survey_date, planting_date):
        return (survey_date - planting_date).days
    
    def getVersion(DAP, county):
        #['Homabay', 'Bungoma', 'Busia', 'migori', 'Baringo', 'Kilifi', 'Siaya']
        if county == "migori":
            if DAP <= 25:
                return 1
            return 2
        elif county == "Homabay" or county == "Busia" or county == "Baringo" or county == "Kilifi" or county == "Bungoma":
            if DAP <= 15:
                return 1
            return 2
        elif county == "Siaya":
            if DAP <= 16:
                return 1
            return 2
        
    # load planing date information for all farms/ # change later
    try:
        planting_date = pd.read_csv("output/cassava_sos_planting_survey.csv")
    except:
        os.system("python3 code/cassava_sos/planting_survey.py")
        planting_date = pd.read_csv("output/cassava_sos_planting_survey.csv")

    # standardize ID
    data["farm_id"] =data["farm_id"].apply(standardizeFarmID); planting_date["farm_id"] = planting_date["farm_id"].apply(standardizeFarmID)

    data = planting_date[["farm_id", "planting_date"]].merge(data, on="farm_id")

    # date format surveys 
    data["planting_date"] = pd.to_datetime(data["planting_date"]); data["survey_date"] = pd.to_datetime(data["date"])

    # get Days after planting for which all the surveys were done
    data["DAP"] = data.apply(lambda x: getDAP(x["survey_date"], x["planting_date"]), axis=1)

    # add survey version info
    data["survey_version"] = data.apply(lambda x: getVersion(x["DAP"], x["county"]), axis=1)

    return data


def preProcessData(data):
    # generate farm id
    def getUniqueFarmID(county, field_id):
        if field_id < 10:
            return f"{county}:0{field_id}"

        return f"{county}:{field_id}"

    data["farm_id"] = data.apply(lambda x: getUniqueFarmID(x["county"],x["field_id"]), axis=1)

    # germination metrics
    data["germination_rate"] = data["germination_num"]/36; data["germination_percent"] = data["germination_rate"] * 100

    ### add survey version info 
    data = addGerminationVersionInfo(data)

    # reduce the columns 
    filter_cols = ['block','plot','treatment','biochar_rate','cassav_variety','germination_num','erosion','holes_affected_by_erosion','termites','holes_affected','SubmissionDate','date','county','field_id','location-Latitude','location-Longitude','location-Altitude','location-Accuracy','farm_id','survey_version','germination_percent']
    data = data[filter_cols]

    return data


def main():
    form_url = "https://opendatakit.plantvillage.psu.edu/v1/projects/265/forms/Cassava-SOS-Germination-Survey/"
    data = downloadFiles(form_url)
    processed_data = preProcessData(data) # preprocess data
    processed_data.to_csv("output/cassava_sos_germination_survey.csv")


if __name__ == "__main__":
    main()