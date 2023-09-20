#!/usr/bin/env python3

import datetime
import os
import shutil
import subprocess
import sys

import numpy as np
import pandas as pd

from common import farm_id, farm_num_id, load_aez
import odkcentral as odk


def downloadFiles(form_url: str) -> pd.DataFrame:
    """Download CSV data from ODK using url"""
    def get_block(plot):
        if plot < 9:
            return 1
        else:
            return 2
        
    # download data from ODK
    folder = odk.download_submissions(form_url)

    # load data
    plots = pd.read_csv(folder / "Cassava-SOS-Canopy-Measurement-plot.csv")
    plants = pd.read_csv(folder / "Cassava-SOS-Canopy-Measurement-plant.csv")
    farms = pd.read_csv(folder / "Cassava-SOS-Canopy-Measurement.csv")

    # merge plots to farms
    farms["PARENT_KEY"] = farms["KEY"]
    data = farms[["date", "map", "county", "farm_id", "PARENT_KEY"]].merge(plots, on="PARENT_KEY")

    # Add block information 
    data["block"] = data.number.apply(get_block)

    # merge plants to plots and farms
    data["PARENT_KEY"] = data["KEY"]
    data = data.merge(plants, on="PARENT_KEY")
    
    shutil.rmtree(folder)

    # return plant level data
    return data


def add_ecological_zones(data: pd.DataFrame) -> pd.DataFrame:
    data = load_aez(data)

    return data[[
        'zones',
        'farm_id',
        'field_id',
        'date',
        'map',
        'county',
        'number',
        'treatment',
        'biochar',
        'variety',
        'block',
        'num',
        'stem_number',
        'plant_height',
        'canopy_height',
        'stem_diameter',
        'branches',
        'nbl',
        'hgt',
        'nodes'
    ]]


def preProcessData(data: pd.DataFrame) -> pd.DataFrame:    
    data["field_id"] = data["farm_id"]
    data["farm_id"] = data.apply(lambda x: farm_id(x["county"], x["farm_id"]), axis=1)  
    return add_ecological_zones(data)


def main() -> None:
    form_url = "https://opendatakit.plantvillage.psu.edu/v1/projects/265/forms/Cassava-SOS-Canopy-Measurement/"
    data = downloadFiles(form_url)
    processed_data = preProcessData(data) # preprocess data
    processed_data.to_csv("output/cassava_sos_canopy_analysis.csv", index=False)


if __name__ == "__main__":
    main()