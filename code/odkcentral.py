import json
import requests
import zipfile

# Needs a bearer token to interact with the API
def getBearerToken(url: str, auth: str):
    headers = {
      'Content-Type': 'application/json'
    }
    r = requests.post(sessions_url, data = json.dumps(auth), headers=headers)
    return eval(r.text)['token']


# Replace auth with personal authentifications
file = open('module/credentials.json') # json file with password and username
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


def downloadSubmissions(form_url, headers=headers) -> str:
    download_url = form_url + "submissions.csv.zip"
    form_file = f'odk_temp_download/{form_url.split("/")[-2]}.zip'
    params = {
        'attachments': False,
        '$filter': "__system/reviewState ne 'rejected' and __system/reviewState ne 'hasIssues'"
    }
    try:
        r = requests.get(download_url, headers=headers, stream=True, params=params)
        with open(form_file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=512):
                if chunk:
                    f.write(chunk)

        with zipfile.ZipFile(form_file, "r") as zip_ref:
            zip_ref.extractall(f"odk_temp_download/{form_url.split('/')[-2]}")
    except:
        print("Failed to download new")
        pass

    return f'odk_temp_download/{form_url.split("/")[-2]}'
