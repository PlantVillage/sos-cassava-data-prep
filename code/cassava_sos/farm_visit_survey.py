#!/usr/bin/env python3

import datetime
import os
import sys

import numpy as np
import pandas as pd

from common import days_after_planting, standardize_farm_id

# import odkcentral
sys.path.insert(0, "module") # relative path to the module folder
import odkcentral as odk


# download odk central files
def downloadFiles(form_url):
    folder = odk.downloadSubmissions(form_url)

    # set path
    path = f"{folder}/{os.listdir(folder)[0]}"

    # load data
    data = pd.read_csv(path)

    # remove rejected and has issues surveys
    data = data[data["ReviewState"] != 'rejected']
    data = data[data["ReviewState"] != 'hasIssues'] 

    return data # return merged data, where each row is data for a plot


def renameColumns(data):
    cols = [
        'experimental_data-plot_data-experimental_field-termite_number',
        'experimental_data-plot_data-experimental_field-soil_number',
        'experimental_data-plot_data-experimental_field-biochar_run_off_number',
        'experimental_data-plot_data-experimental_field-water_logging_number',
        'experimental_data-plot_data-experimental_field-weed_pressure',
        'experimental_data-plot_data-experimental_field-animal_damage_number',
        'experimental_data-plot_data-experimental_field-germination',
        'experimental_data-plot_data-experimental_field-plot_image',
        'experimental_data-plot_data-experimental_field2-termite_number2',
        'experimental_data-plot_data-experimental_field2-soil_number2',
        'experimental_data-plot_data-experimental_field2-biochar_run_off_number2',
        'experimental_data-plot_data-experimental_field2-water_logging_number2',
        'experimental_data-plot_data-experimental_field2-weed_pressure2',
        'experimental_data-plot_data-experimental_field2-animal_damage_number2',
        'experimental_data-plot_data-experimental_field2-germination2',
        'experimental_data-plot_data-experimental_field2-plot_image2',
        'experimental_data-plot_data-experimental_field3-termite_number3',
        'experimental_data-plot_data-experimental_field3-soil_number3',
        'experimental_data-plot_data-experimental_field3-biochar_run_off_number3',
        'experimental_data-plot_data-experimental_field3-water_logging_number3',
        'experimental_data-plot_data-experimental_field3-weed_pressure3',
        'experimental_data-plot_data-experimental_field3-animal_damage_number3',
        'experimental_data-plot_data-experimental_field3-germination3',
        'experimental_data-plot_data-experimental_field3-plot_image3',
        'experimental_data-plot_data-experimental_field4-termite_number4',
        'experimental_data-plot_data-experimental_field4-soil_number4',
        'experimental_data-plot_data-experimental_field4-biochar_run_off_number4',
        'experimental_data-plot_data-experimental_field4-water_logging_number4',
        'experimental_data-plot_data-experimental_field4-weed_pressure4',
        'experimental_data-plot_data-experimental_field4-animal_damage_number4',
        'experimental_data-plot_data-experimental_field4-germination4',
        'experimental_data-plot_data-experimental_field4-plot_image4',
        'experimental_data-plot_data-experimental_field5-termite_number5',
        'experimental_data-plot_data-experimental_field5-soil_number5',
        'experimental_data-plot_data-experimental_field5-biochar_run_off_number5',
        'experimental_data-plot_data-experimental_field5-water_logging_number5',
        'experimental_data-plot_data-experimental_field5-weed_pressure5',
        'experimental_data-plot_data-experimental_field5-animal_damage_number5',
        'experimental_data-plot_data-experimental_field5-germination5',
        'experimental_data-plot_data-experimental_field5-plot_image5',
        'experimental_data-plot_data-experimental_field6-termite_number6',
        'experimental_data-plot_data-experimental_field6-soil_number6',
        'experimental_data-plot_data-experimental_field6-biochar_run_off_number6',
        'experimental_data-plot_data-experimental_field6-water_logging_number6',
        'experimental_data-plot_data-experimental_field6-weed_pressure6',
        'experimental_data-plot_data-experimental_field6-animal_damage_number6',
        'experimental_data-plot_data-experimental_field6-germination6',
        'experimental_data-plot_data-experimental_field6-plot_image6',
        'experimental_data-plot_data-experimental_field7-termite_number7',
        'experimental_data-plot_data-experimental_field7-soil_number7',
        'experimental_data-plot_data-experimental_field7-biochar_run_off_number7',
        'experimental_data-plot_data-experimental_field7-water_logging_number7',
        'experimental_data-plot_data-experimental_field7-weed_pressure7',
        'experimental_data-plot_data-experimental_field7-animal_damage_number7',
        'experimental_data-plot_data-experimental_field7-germination7',
        'experimental_data-plot_data-experimental_field7-plot_image7',
        'experimental_data-plot_data-experimental_field8-termite_number8',
        'experimental_data-plot_data-experimental_field8-soil_number8',
        'experimental_data-plot_data-experimental_field8-biochar_run_off_number8',
        'experimental_data-plot_data-experimental_field8-water_logging_number8',
        'experimental_data-plot_data-experimental_field8-weed_pressure8',
        'experimental_data-plot_data-experimental_field8-animal_damage_number8',
        'experimental_data-plot_data-experimental_field8-germination8',
        'experimental_data-plot_data-experimental_field8-plot_image8',
        'experimental_data-plot_data-experimental_field9-termite_number9',
        'experimental_data-plot_data-experimental_field9-soil_number9',
        'experimental_data-plot_data-experimental_field9-biochar_run_off_number9',
        'experimental_data-plot_data-experimental_field9-water_logging_number9',
        'experimental_data-plot_data-experimental_field9-weed_pressure9',
        'experimental_data-plot_data-experimental_field9-animal_damage_number9',
        'experimental_data-plot_data-experimental_field9-germination9',
        'experimental_data-plot_data-experimental_field9-plot_image9',
        'experimental_data-plot_data-experimental_field10-termite_number10',
        'experimental_data-plot_data-experimental_field10-soil_number10',
        'experimental_data-plot_data-experimental_field10-biochar_run_off_number10',
        'experimental_data-plot_data-experimental_field10-water_logging_number10',
        'experimental_data-plot_data-experimental_field10-weed_pressure10',
        'experimental_data-plot_data-experimental_field10-animal_damage_number10',
        'experimental_data-plot_data-experimental_field10-germination10',
        'experimental_data-plot_data-experimental_field10-plot_image10',
        'experimental_data-plot_data-experimental_field11-termite_number11',
        'experimental_data-plot_data-experimental_field11-soil_number11',
        'experimental_data-plot_data-experimental_field11-biochar_run_off_number11',
        'experimental_data-plot_data-experimental_field11-water_logging_number11',
        'experimental_data-plot_data-experimental_field11-weed_pressure11',
        'experimental_data-plot_data-experimental_field11-animal_damage_number11',
        'experimental_data-plot_data-experimental_field11-germination11',
        'experimental_data-plot_data-experimental_field11-plot_image11',
        'experimental_data-plot_data-experimental_field12-termite_number12',
        'experimental_data-plot_data-experimental_field12-soil_number12',
        'experimental_data-plot_data-experimental_field12-biochar_run_off_number12',
        'experimental_data-plot_data-experimental_field12-water_logging_number12',
        'experimental_data-plot_data-experimental_field12-weed_pressure12',
        'experimental_data-plot_data-experimental_field12-animal_damage_number12',
        'experimental_data-plot_data-experimental_field12-germination12',
        'experimental_data-plot_data-experimental_field12-plot_image12',
        'experimental_data-plot_data-experimental_field13-termite_number13',
        'experimental_data-plot_data-experimental_field13-soil_number13',
        'experimental_data-plot_data-experimental_field13-biochar_run_off_number13',
        'experimental_data-plot_data-experimental_field13-water_logging_number13',
        'experimental_data-plot_data-experimental_field13-weed_pressure13',
        'experimental_data-plot_data-experimental_field13-animal_damage_number13',
        'experimental_data-plot_data-experimental_field13-germination13',
        'experimental_data-plot_data-experimental_field13-plot_image13',
        'experimental_data-plot_data-experimental_field14-termite_number14',
        'experimental_data-plot_data-experimental_field14-soil_number14',
        'experimental_data-plot_data-experimental_field14-biochar_run_off_number14',
        'experimental_data-plot_data-experimental_field14-water_logging_number14',
        'experimental_data-plot_data-experimental_field14-weed_pressure14',
        'experimental_data-plot_data-experimental_field14-animal_damage_number14',
        'experimental_data-plot_data-experimental_field14-germination14',
        'experimental_data-plot_data-experimental_field14-plot_image14',
        'experimental_data-plot_data-experimental_field15-termite_number15',
        'experimental_data-plot_data-experimental_field15-soil_number15',
        'experimental_data-plot_data-experimental_field15-biochar_run_off_number15',
        'experimental_data-plot_data-experimental_field15-water_logging_number15',
        'experimental_data-plot_data-experimental_field15-weed_pressure15',
        'experimental_data-plot_data-experimental_field15-animal_damage_number15',
        'experimental_data-plot_data-experimental_field15-germination15',
        'experimental_data-plot_data-experimental_field15-plot_image15',
        'experimental_data-plot_data-experimental_field16-termite_number16',
        'experimental_data-plot_data-experimental_field16-soil_number16',
        'experimental_data-plot_data-experimental_field16-biochar_run_off_number16',
        'experimental_data-plot_data-experimental_field16-water_logging_number16',
        'experimental_data-plot_data-experimental_field16-weed_pressure16',
        'experimental_data-plot_data-experimental_field16-animal_damage_number16',
        'experimental_data-plot_data-experimental_field16-germination16',
        'experimental_data-plot_data-experimental_field16-plot_image16'
    ]

    cols1 = [col.split("-")[-1] for col in cols]

    dict1 = {}
    for i in range(len(cols)):
        col = cols[i]
        dict1[col] = cols1[i]

    data = data.rename(columns=dict1)

    return data

def preProcessFarmData(data):
    # generate farm id
    def getUniqueFarmID(county, field_id):
        try:
            if field_id < 10:
                return f"{county.lower()}:0{int(field_id)}"

            return f"{county.lower()}:{int(field_id)}"
        except:
            return "Unknown"
    
    # enable the date format
    data['date']= pd.to_datetime(data['date'])

    data["farm_id"] = data.apply(lambda x: getUniqueFarmID(x["county"], x["field_id"]), axis=1)

    # rename columns 
    data = renameColumns(data)

    return data


def farmVistSurvey(data):
    processed_data = preProcessFarmData(data) # preprocess data
    processed_data.to_csv("output/cassava_sos_farm_visit_survey.csv")
    return processed_data


def preProcessPlotData(data):
    plot_col_base = [
        'termite_number',
        'soil_number',
        'biochar_run_off_number',
        'water_logging_number',
        'weed_pressure',
        'animal_damage_number',
        'germination',
        'plot_image',
        "plot_number"
    ]
    
    def getColBase(col, index):
        if "plot_number" in col:
            return "plot_number"
        return col.replace(str(index), "")
    
    data = data[data["experimental_data-plot_collection"]== 'Yes']

    data["PARENT_KEY"] = data["KEY"]
    data["plot_number"] = np.arange(len(data))

    # loop through the rows using iterrows()
    data2 = pd.DataFrame()

    for index, row in data.iterrows():
        for i in range(1,17):
            if i == 1:
                temp_df = row[plot_col_base + ["PARENT_KEY"]]
                temp_df["plot_number"] = 1 # chnage plot number
                try:
                    data2 = data2.append(temp_df)
                except:
                    data2 = data2._append(temp_df)
            else:
                cols = [f"{col}{i}" for col in plot_col_base] + ["PARENT_KEY"]
                cols = [col if "plot_number" not in col else "plot_number" for col in cols]
  
                temp_df = row[cols]
                replace_dict = {}
                for col in cols:
                    replace_dict[col] = getColBase(col,i)
                temp_df = temp_df.rename(replace_dict)
                temp_df["plot_number"] = i
                try:
                    data2 = data2.append(temp_df)
                except:
                    data2 = data2._append(temp_df)

    return data2 


def addSurveyVersion(dt):
    planting_date = pd.read_csv("output/cassava_sos_planting_survey.csv")

    # standardize ID
    dt["farm_id"] = dt["farm_id"].apply(standardize_farm_id)
    planting_date["farm_id"] = planting_date["farm_id"].apply(standardize_farm_id)

    dt1 = planting_date[["farm_id", "planting_date"]].merge(dt, on="farm_id")

    # date format surveys 
    dt1["planting_date"] = pd.to_datetime(dt1["planting_date"])
    dt1["survey_date"] = pd.to_datetime(dt1["date"])

    dt1["DAP"] = \
        dt1.apply(lambda x: days_after_planting(x["survey_date"], x["planting_date"]), axis=1)

    def get_version(days_after_planting: int) -> str:
        if days_after_planting in np.arange(41, 51):
            return "45_DAP"
        elif days_after_planting in np.arange(55, 66):
            return "60_DAP"
        elif days_after_planting in np.arange(70, 81):
            return "75_DAP"
        elif days_after_planting in np.arange(85, 96):
            return "90_DAP"
    
    dt1["survey_version"] = dt1["DAP"].apply(get_version)

    return dt1

    
    
def farmPlotVisitSurvey(data):
    plot_columns = [
        'termite_number',
        'soil_number',
        'biochar_run_off_number',
        'water_logging_number',
        'weed_pressure',
        'animal_damage_number',
        'germination',
        'plot_image',
        'termite_number2',
        'soil_number2',
        'biochar_run_off_number2',
        'water_logging_number2',
        'weed_pressure2',
        'animal_damage_number2',
        'germination2',
        'plot_image2',
        'termite_number3',
        'soil_number3',
        'biochar_run_off_number3',
        'water_logging_number3',
        'weed_pressure3',
        'animal_damage_number3',
        'germination3',
        'plot_image3',
        'termite_number4',
        'soil_number4',
        'biochar_run_off_number4',
        'water_logging_number4',
        'weed_pressure4',
        'animal_damage_number4',
        'germination4',
        'plot_image4',
        'termite_number5',
        'soil_number5',
        'biochar_run_off_number5',
        'water_logging_number5',
        'weed_pressure5',
        'animal_damage_number5',
        'germination5',
        'plot_image5',
        'termite_number6',
        'soil_number6',
        'biochar_run_off_number6',
        'water_logging_number6',
        'weed_pressure6',
        'animal_damage_number6',
        'germination6',
        'plot_image6',
        'termite_number7',
        'soil_number7',
        'biochar_run_off_number7',
        'water_logging_number7',
        'weed_pressure7',
        'animal_damage_number7',
        'germination7',
        'plot_image7',
        'termite_number8',
        'soil_number8',
        'biochar_run_off_number8',
        'water_logging_number8',
        'weed_pressure8',
        'animal_damage_number8',
        'germination8',
        'plot_image8',
        'termite_number9',
        'soil_number9',
        'biochar_run_off_number9',
        'water_logging_number9',
        'weed_pressure9',
        'animal_damage_number9',
        'germination9',
        'plot_image9',
        'termite_number10',
        'soil_number10',
        'biochar_run_off_number10',
        'water_logging_number10',
        'weed_pressure10',
        'animal_damage_number10',
        'germination10',
        'plot_image10',
        'termite_number11',
        'soil_number11',
        'biochar_run_off_number11',
        'water_logging_number11',
        'weed_pressure11',
        'animal_damage_number11',
        'germination11',
        'plot_image11',
        'termite_number12',
        'soil_number12',
        'biochar_run_off_number12',
        'water_logging_number12',
        'weed_pressure12',
        'animal_damage_number12',
        'germination12',
        'plot_image12',
        'termite_number13',
        'soil_number13',
        'biochar_run_off_number13',
        'water_logging_number13',
        'weed_pressure13',
        'animal_damage_number13',
        'germination13',
        'plot_image13',
        'termite_number14',
        'soil_number14',
        'biochar_run_off_number14',
        'water_logging_number14',
        'weed_pressure14',
        'animal_damage_number14',
        'germination14',
        'plot_image14',
        'termite_number15',
        'soil_number15',
        'biochar_run_off_number15',
        'water_logging_number15',
        'weed_pressure15',
        'animal_damage_number15',
        'germination15',
        'plot_image15',
        'termite_number16',
        'soil_number16',
        'biochar_run_off_number16',
        'water_logging_number16',
        'weed_pressure16',
        'animal_damage_number16',
        'germination16',
        'plot_image16'
    ]
    expanded_data = preProcessPlotData(data)

    # filter out data with survey with plot data
    data = data[data["experimental_data-plot_collection"]== 'Yes']

    # remove extra columns
    data = data.drop(plot_columns, axis=1)

    # merge plot data with farm
    data["PARENT_KEY"] = data["KEY"]
    data = data.merge(expanded_data, on="PARENT_KEY")

    # add farm_Id 
    farm = pd.read_csv("output/cassava_sos_farm_visit_survey.csv")
    data1 = farm[["KEY", "farm_id"]].merge(data)

    # survey version
    data2 = addSurveyVersion(data1)

    data2.to_csv("output/cassava_sos_farm_visit_plot_survey.csv")


def main():
    form_url = "https://opendatakit.plantvillage.psu.edu/v1/projects/265/forms/Cassava-SOS-Farm-Visit-Survey/"
    data = downloadFiles(form_url)
    processed_data = farmVistSurvey(data)
    farmPlotVisitSurvey(processed_data)
    

if __name__ == "__main__":
    main()