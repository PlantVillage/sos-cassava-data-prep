#!/usr/bin/env python3

import datetime
import os
import sys

import numpy as np
import pandas as pd

from common import farm_id

# import odkcentral
sys.path.insert(0, "module") # relative path to the module folder
import odkcentral as odk


def downloadFiles(form_url):
    '''Download CSV data from ODK using url'''
    def getBlock(plot):
        if plot < 9:
            return 1
        else:
            return 2
        
    # download data from ODK
    folder = odk.downloadSubmissions(form_url)

    # load data
    plots = pd.read_csv(f"{folder}/{os.listdir(folder)[2]}")
    plants = pd.read_csv(f"{folder}/{os.listdir(folder)[1]}")
    farms = pd.read_csv(f"{folder}/{os.listdir(folder)[0]}")

    # filter rejected submission
    farms = farms[farms["ReviewState"] != "hasIssues"]
    farms = farms[farms["ReviewState"] != "rejected"]

    # merge plots to farms
    farms["PARENT_KEY"] = farms["KEY"]
    data = farms[["date","map","county","farm_id", "PARENT_KEY"]].merge(plots, on="PARENT_KEY")

    # Add block information 
    data["block"] = data.number.apply(getBlock)

    # merge plants to plots and farms
    data["PARENT_KEY"] = data["KEY"]
    data = data.merge(plants, on="PARENT_KEY")
    
    # return plant level data
    return data


def addEcologicalZones(data):
    '''
    Add agro-ecological zone info to data based on farm_id
    '''
    try:
        # Add Agro-Ecological Zone Information
        df = pd.read_csv("output/cassava_sos_planting_survey.csv")
    except:
        os.system("python code/cassava_sos/planting_survey.py")
        df = pd.read_csv("output/cassava_sos_planting_survey.csv")

    def getID(id):
        return int(id.split(":")[1])

    df["num_id"] = df["farm_id"].apply(getID)

    df["farm_id"] = df.apply(lambda x: farm_id(x['farm_id'], x['num_id']), axis=1)


    # get zone data from planting report survey
    aez = {}
    for id in df["farm_id"].unique().tolist():
        zone = df.query(f" farm_id == '{id}'")["zones"].unique().tolist()[0]
        aez[id] = zone

    # function to return aez for farms
    def getAEZ(id):
        return aez[id]

    data["zones"] = data["farm_id"].apply(getAEZ)



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
                'nodes']]



def preProcessData(data):

    #print("\nProcessing files ....\n")

    # Create Farm ID
    def getFarmID(county, id):
        if "Baringo" in county:
            if id < 10:
                return f"BAR:0{id}"
            return f"BAR:{id}"
        elif "Siaya" in county:
            if id < 10:
                return f"SIA:0{id}"
            return f"SIA:{id}"
        elif "Homabay" in county:
            if id < 10:
                return f"HOM:0{id}"
            return f"HOM:{id}"
        elif "Bungoma" in county:
            if id < 10:
                return f"BUN:0{id}"
            return f"BUN:{id}"
        elif "Busia" in county:
            if id < 10:
                return f"BUS:0{id}"
            return f"BUS:{id}"
        elif "Migori" in county:
            if id < 10:
                return f"MIG:0{id}"
            return f"MIG:{id}"
        elif "Kilifi" in county:
            if id < 10:
                return f"KIL:0{id}"
            return f"KIL:{id}"
        
    # add farm id information to data
    data["field_id"] = data["farm_id"]
    data["farm_id"] = data.apply(lambda x: getFarmID(x["county"], x["farm_id"]), axis=1)
    
    return addEcologicalZones(data)


def main():
    form_url = "https://opendatakit.plantvillage.psu.edu/v1/projects/265/forms/Cassava-SOS-Canopy-Measurement/"
    data = downloadFiles(form_url)
    processed_data = preProcessData(data) # preprocess data
    processed_data.to_csv("output/cassava_sos_canopy_analysis.csv")


if __name__ == "__main__":
    main()