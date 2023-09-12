#!/usr/bin/env python3

import datetime
import os
import sys

import numpy as np
import pandas as pd

from common import farm_id, farm_num_id

# import odkcentral
sys.path.insert(0, "module") # relative path to the module folder
import odkcentral as odk

def downloadFiles(form_url):

    #print("\nDownloading files ....\n")

    folder = odk.downloadSubmissions(form_url)

    plots = pd.read_csv(f"{folder}/{os.listdir(folder)[0]}")
    plants = pd.read_csv(f"{folder}/{os.listdir(folder)[1]}")
    farms = pd.read_csv(f"{folder}/{os.listdir(folder)[2]}")

    farms = farms[farms["ReviewState"] != "hasIssues"]
    farms = farms[farms["ReviewState"] != "rejected"]

    # add merge plots to farms
    farms["PARENT_KEY"] = farms["KEY"]
    data = farms[["date", "map", "county", "field_id", "PARENT_KEY"]].merge(plots, on="PARENT_KEY")

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

    df["num_id"] = df["farm_id"].apply(farm_num_id)
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
        'date',
        'map',
        'county',
        'field_id',
        'plot_number',
        'block_number',
        'biochar_level',
        'treanment_applied',
        'variey',
        'stand_count',
        'total_net_count',
        'cmd_incidence_net',
        'cmd_incidence_out',
        'cbsd_incidence_net',
        'cbsd_incidence_out',
        'plant_number',
        'cmd_severity',
        'cbsd_severity',
        'stem_count',
        'cmd_systemicity',
        'cbsd_systemicity',
        'farm_id',
        'biochar',
        'zones'
    ]]



def preProcessData(data):
    data["farm_id"] = data.apply(lambda x: farm_id(x["county"], x["field_id"]), axis=1)
    
    # fix issues with columns 
    cols = {
        'cmd_incidence': "cmd_incidence_net",
        'cmd_incidence.' : "cmd_incidence_out",
        'cbsd_incidence.' : "cbsd_incidence_net",
        'cbsd_incidence' : "cbsd_incidence_out",
    }
    data = data.rename(columns=cols)

    # fix biochar level 
    def stdBiochar(level):
        if "10" in level:
            return 10
        elif "5" in level:
            return 5
        elif "0" in level:
            return 0

    data["biochar"] = data["biochar_level"].apply(stdBiochar)

    # analyze systemacity 

    data["cmd_systemicity"] = \
        (data["cmd_systemicity"] / data["stem_count"]) * 100
    data["cbsd_systemicity"] = \
        (data["cbsd_systemicity"] / data["stem_count"]) * 100
    data["cmd_incidence_net"] = \
        (data["cmd_incidence_net"] / data["total_net_count"]) * 100
    data["cbsd_incidence_net"] = \
        (data["cbsd_incidence_net"] / data["total_net_count"]) * 100
    data["cmd_incidence_out"] = \
        (data["cmd_incidence_out"] / (data["stand_count"] - data["total_net_count"])) * 100
    data["cbsd_incidence_out"] = \
        (data["cmd_incidence_out"] / (data["stand_count"] - data["total_net_count"])) * 100

    return addEcologicalZones(data)


def main():
    form_url = "https://opendatakit.plantvillage.psu.edu/v1/projects/265/forms/Cassava-SOS-Disease-Evaluation-Score-Survey-Form/"
    data = downloadFiles(form_url)
    processed_data = preProcessData(data) # preprocess data
    processed_data.to_csv("output/cassava_sos_disease_monitoring.csv")


if __name__ == "__main__":
    main()