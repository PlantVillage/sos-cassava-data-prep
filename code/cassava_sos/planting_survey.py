# import python modules
import os
import geopandas as gpd
import pandas as pd
import numpy as np
import datetime
import sys

# import odkcentral
sys.path.insert(0, "module") # relative path to the module folder
import odkcentral as odk


# download odk central files
def downloadFiles(form_url):
    folder = odk.downloadSubmissions(form_url)
    #print(os.listdir(folder))

    # set path
    path = f"{folder}/{os.listdir(folder)[1]}"

    # load data
    data = pd.read_csv(path)

    # remove rejected and has issues surveys
    data = data[data["ReviewState"] != 'rejected']; data = data[data["ReviewState"] != 'hasIssues'] 

    return data # return merged data, where each row is data for a plot



def addAgroEcologicalZones(data):
    # Read shapefile
    kenya_aez = gpd.read_file("/Users/edwardamoah/Documents/GitHub/cetcil_data_analysis/cetcil/JupyterCode/data/static/kenya_aez/Kenya_AgroEcolZones.shp")

    gdf = gpd.GeoDataFrame( data, geometry= gpd.points_from_xy(data['location-Longitude'], data['location-Latitude']))

    # join spatial data with odk data
    data = gpd.sjoin(kenya_aez, gdf)

    return data
    

def preProcessData(data):
    # generate farm id
    def getUniqueFarmID(county, field_id):
        if field_id < 10:
            return f"{county}:0{field_id}"

        return f"{county}:{field_id}"
    
    # enable the date format
    data['planting_date']= pd.to_datetime(data['planting_date'])

    # change county_name column
    data["county"] = data["county_name"]

    data["farm_id"] = data.apply(lambda x: getUniqueFarmID(x["county"],x["field_id"]), axis=1)

    # add agroEcologicalZones
    data = addAgroEcologicalZones(data)

    return data



def main():
    form_url = "https://opendatakit.plantvillage.psu.edu/v1/projects/265/forms/Cassava-SOS-Planting-Report/"
    data = downloadFiles(form_url)
    processed_data = preProcessData(data) # preprocess data
    processed_data.to_csv("output/cassava_sos_planting_survey.csv")


if __name__ == "__main__":
    main()