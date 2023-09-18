#!/usr/bin/env python3

import datetime
import os
import sys

import geopandas as gpd
import numpy as np
import pandas as pd

from common import unique_farm_id
import odkcentral as odk


def downloadFiles(form_url: str) -> pd.DataFrame:
    folder = odk.downloadSubmissions(form_url)
    path = f"{folder}/Cassava-SOS-Planting-Report.csv"
    data = pd.read_csv(path)
    return data


def addAgroEcologicalZones(data):
    kenya_aez = gpd.read_file("kenya_aez/Kenya_AgroEcolZones.shp")

    gdf = gpd.GeoDataFrame(
        data, 
        geometry=gpd.points_from_xy(data['location-Longitude'], data['location-Latitude']),
        crs="EPSG:4326"
    )

    # join spatial data with odk data
    data = gpd.sjoin(kenya_aez, gdf)

    return data
    

def preProcessData(data: pd.DataFrame) -> pd.DataFrame:
    data['planting_date']= pd.to_datetime(data['planting_date'])
    data["county"] = data["county_name"]
    data["farm_id"] =\
        data.apply(lambda x: unique_farm_id(x["county"], x["field_id"]), axis=1)

    data = addAgroEcologicalZones(data)
    return data


def main() -> None:
    form_url = "https://opendatakit.plantvillage.psu.edu/v1/projects/265/forms/Cassava-SOS-Planting-Report/"
    data = downloadFiles(form_url)
    processed_data = preProcessData(data)
    processed_data.to_csv("output/cassava_sos_planting_survey.csv")


if __name__ == "__main__":
    main()