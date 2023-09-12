#!/usr/bin/env python3

import datetime
import os
import sys

import numpy as np
import pandas as pd

# import odkcentral
sys.path.insert(0, "module") # relative path to the module folder
import odkcentral as odk


def downloadFiles(form_url):
    folder = odk.downloadSubmissions(form_url)

    farms = pd.read_csv(f"{folder}/{os.listdir(folder)[0]}")
    plants = pd.read_csv(f"{folder}/{os.listdir(folder)[1]}")
    plots = pd.read_csv(f"{folder}/{os.listdir(folder)[2]}")

    # filter out rejected and submission with issues
    farms = farms[farms["ReviewState"] != "hasIssues"]
    farms = farms[farms["ReviewState"] != "rejected"]

    # Merge plants, and plot data to farms

    # add merge plots to farms
    farms["PARENT_KEY"] = farms["KEY"]
    data = farms[["date","map","county","field_id", "PARENT_KEY"]].merge(plots, on="PARENT_KEY")

    # merge plants to plots and farms
    data["PARENT_KEY"] = data["KEY"]
    data = data.merge(plants, on="PARENT_KEY")

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

    def getID(id):
        return int(id.split(":")[1])

    df["num_id"] = df["farm_id"].apply(getID)

    df["farm_id"] = df.apply(lambda x: getFarmID(x['farm_id'], x['num_id']), axis=1)


    # get zone data from planting report survey
    aez = {}
    for id in df["farm_id"].unique().tolist():
        zone = df.query(f" farm_id == '{id}'")["zones"].unique().tolist()[0]
        aez[id] = zone

    # function to return aez for farms
    def getAEZ(id):
        return aez[id]

    data["zones"] = data["farm_id"].apply(getAEZ)



    return data[['date',
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
                'zones']]

def preProcessData(data):

    #print("\nProcessing files ....\n")

    # add farmID
    def getFarmID(county, id):
        if "baringo" in county:
            if id < 10:
                return f"BAR:0{id}"
            return f"BAR:{id}"
        elif "siaya" in county:
            if id < 10:
                return f"SIA:0{id}"
            return f"SIA:{id}"
        elif "homabay" in county:
            if id < 10:
                return f"HOM:0{id}"
            return f"HOM:{id}"
        elif "bungoma" in county:
            if id < 10:
                return f"BUN:0{id}"
            return f"BUN:{id}"
        elif "busia" in county:
            if id < 10:
                return f"BUS:0{id}"
            return f"BUS:{id}"
        elif "migori" in county:
            if id < 10:
                return f"MIG:0{id}"
            return f"MIG:{id}"
        elif "kilifi" in county:
            if id < 10:
                return f"KIL:0{id}"
            return f"KIL:{id}"
        

    data["farm_id"] = data.apply(lambda x: getFarmID(x["county"], x["field_id"]), axis=1)
    
    return addEcologicalZones(data)


def main():
    form_url = "https://opendatakit.plantvillage.psu.edu/v1/projects/265/forms/Whitefly-Image-Data-Collection/"
    data = downloadFiles(form_url)
    processed_data = preProcessData(data) # preprocess data
    processed_data.to_csv("output/cassava_sos_whitefly_monitoring.csv")


if __name__ == "__main__":
    main()