import requests
import json
import zipfile
import pandas as pd

# Needs a bearer token to interact with the API
def getBearerToken(url, auth):
    headers = {
      'Content-Type': 'application/json'
    }
    r = requests.post(sessions_url, data = json.dumps(auth), headers=headers)
    return eval(r.text)['token']


# Replace auth with personal authentifications
file = open('/Users/edwardamoah/Documents/GitHub/cetcil_data_analysis/cetcil/JupyterCode/notebooks/credentialPV.json') # json file with password and username
auth = json.load(file)

sessions_url = "https://opendatakit.plantvillage.psu.edu/v1/sessions"

bearerToken = ""

# get tokens
try:
    bearerToken = getBearerToken(sessions_url, auth)
except:
    print("Unable to establish connection to server")

headers = {
  'Content-Type': 'application/json',
  'Authorization': f'Bearer {bearerToken}'
}


def downloadSubmissions1(form_url, headers):
    download_url = form_url + f"submissions.csv.zip?attachments=false"
    form_file = f'{form_url.split("/")[-2]}.zip'
    r = requests.post(download_url, headers=headers, stream=True)
    with open(form_file, 'wb') as f:
        for chunk in r.iter_content(chunk_size=512):
            if chunk:
                f.write(chunk)

    # unzip downloaded folder
    with zipfile.ZipFile(form_file,"r") as zip_ref:
        zip_ref.extractall("")

    return pd.read_csv(f'{form_url.split("/")[-2]}.csv')

def downloadSubmissions(form_url, headers=headers):
    download_url = form_url + f"submissions.csv.zip?attachments=false"
    form_file = f'odk_temp_download/{form_url.split("/")[-2]}.zip'
    try:
        r = requests.post(download_url, headers=headers, stream=True)
        with open(form_file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=512):
                if chunk:
                    f.write(chunk)

        # unzip downloaded folder
        with zipfile.ZipFile(form_file,"r") as zip_ref:
            zip_ref.extractall(f"odk_temp_download/{form_url.split('/')[-2]}")
    except:
        print("Failed to downlaod new")
        pass

    return f'odk_temp_download/{form_url.split("/")[-2]}'


def downloadFormSubmissions(form_url, auth=auth):
    if bearerToken == "":
        bearerToken = getBearerToken(sessions_url, auth)

        headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {bearerToken}'
        }

    return downloadSubmissions(form_url, headers)