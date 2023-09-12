#!/usr/bin/env python3

import datetime
import os
import sys

import geopandas as gpd
import numpy as np
import pandas as pd

from common import unique_farm_id


# import odkcentral
sys.path.insert(0, "module") # relative path to the module folder
import odkcentral as odk


# download odk central files
def downloadFiles(form_url):
    folder = odk.downloadSubmissions(form_url)

    # set path
    path = f"{folder}/{os.listdir(folder)[1]}"

    # load data
    data = pd.read_csv(path)

    # remove rejected and has issues surveys
    data = data[data["ReviewState"] != 'rejected']
    data = data[data["ReviewState"] != 'hasIssues'] 

    return data # return merged data, where each row is data for a plot



def addAgroEcologicalZones(data):
    kenya_aez = gpd.read_file("input/kenya_aez/Kenya_AgroEcolZones.shp")

    gdf = gpd.GeoDataFrame( data, geometry= gpd.points_from_xy(data['location-Longitude'], data['location-Latitude']))

    # join spatial data with odk data
    data = gpd.sjoin(kenya_aez, gdf)

    return data
    

def preProcessData(data):
    data['planting_date']= pd.to_datetime(data['planting_date'])
    data["county"] = data["county_name"]
    data["farm_id"] =\
        data.apply(lambda x: unique_farm_id(x["county"], x["field_id"]), axis=1)

    data = addAgroEcologicalZones(data)
    return data


def main():
    form_url = "https://opendatakit.plantvillage.psu.edu/v1/projects/265/forms/Cassava-SOS-Planting-Report/"
    data = downloadFiles(form_url)
    processed_data = preProcessData(data)
    processed_data.to_csv("output/cassava_sos_planting_survey.csv")


if __name__ == "__main__":
    main()