#!/usr/bin/env python3

import datetime
import os
import subprocess
import sys

import numpy as np
import pandas as pd

from common import farm_id, farm_num_id, load_aez
import odkcentral as odk


def downloadFiles(form_url: str) -> pd.DataFrame:
    folder = odk.download_submissions(form_url)

    farms = pd.read_csv(folder / "Whitefly-Image-Data-Collection.csv")
    plants = pd.read_csv(folder / "Whitefly-Image-Data-Collection-plant_image.csv")
    plots = pd.read_csv(folder / "Whitefly-Image-Data-Collection-plot_survey.csv")

    # Merge plants, and plot data to farms

    # add merge plots to farms
    farms["PARENT_KEY"] = farms["KEY"]
    data = farms[["date", "map", "county", "field_id", "PARENT_KEY"]].merge(plots, on="PARENT_KEY")

    # merge plants to plots and farms
    data["PARENT_KEY"] = data["KEY"]
    data = data.merge(plants, on="PARENT_KEY")

    return data


def add_ecological_zones(data: pd.DataFrame) -> pd.DataFrame:
    data = load_aez(data)

    return data[[
        'date',
        'map',
        'county',
        'field_id',
        'plot_number',
        'block_number',
        'biochar_level',
        'trietment_applied',
        'cassava_variety',
        'plant_number',
        'stem_count',
        'farm_id',
        'zones'
    ]]


def preProcessData(data: pd.DataFrame) -> pd.DataFrame:
    data["farm_id"] = data.apply(lambda x: farm_id(x["county"], x["field_id"]), axis=1)  
    return add_ecological_zones(data)


def main():
    form_url = "https://opendatakit.plantvillage.psu.edu/v1/projects/265/forms/Whitefly-Image-Data-Collection/"
    data = downloadFiles(form_url)
    processed_data = preProcessData(data)
    processed_data.to_csv("output/cassava_sos_whitefly_monitoring.csv", index=False)


if __name__ == "__main__":
    main()