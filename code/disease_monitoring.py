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

    plots = pd.read_csv(folder / "Cassava-SOS-Disease-Evaluation-Score-Survey-Form-plot_survey.csv")
    severity = pd.read_csv(folder / "Cassava-SOS-Disease-Evaluation-Score-Survey-Form-severity.csv")
    farms = pd.read_csv(folder / "Cassava-SOS-Disease-Evaluation-Score-Survey-Form.csv")

    # add merge plots to farms
    farms["PARENT_KEY"] = farms["KEY"]
    data = farms[["date", "map", "county", "field_id", "PARENT_KEY"]].merge(plots, on="PARENT_KEY")

    # merge plants to plots and farms
    data["PARENT_KEY"] = data["KEY"]
    data = data.merge(severity, on="PARENT_KEY")
    
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

    return add_ecological_zones(data)


def main():
    form_url = "https://opendatakit.plantvillage.psu.edu/v1/projects/265/forms/Cassava-SOS-Disease-Evaluation-Score-Survey-Form/"
    data = downloadFiles(form_url)
    processed_data = preProcessData(data)
    processed_data.to_csv("output/cassava_sos_disease_monitoring.csv", index=False)


if __name__ == "__main__":
    main()