import json
import os
import requests
import sys
from typing import Optional
import zipfile

def load_from_env(var_name: str) -> str:
    """Load a variable from the OS environment."""
    if not var_name in os.environ:
        print(f'Error: Environment missing {var_name} variable. Aborting.')
        sys.exit(1)
    return os.environ[var_name]


def odk_authenticate(username: str, password: str) -> Optional[str]:
    """
    Try to authenticate to the ODK server and return a session token
    for bearer authentication.
    """
    try:
        url = "https://opendatakit.plantvillage.psu.edu/v1/sessions"
        payload = {'email': username, 'password': password}
        r = requests.post(url, json=payload)
        if r.ok:
            return r.json()['token']
    except HTTPError as http_err:
        print(f"Authentication error: {http_err}")
        return None
    except Exception as e:
        print(f"Authentication error: {e}")
        return None

odk_username = load_from_env('ODK_CENTRAL_USER')
odk_password = load_from_env('ODK_CENTRAL_PASSWORD')

bearerToken = odk_authenticate(odk_username, odk_password)

headers = {
  'Content-Type': 'application/json',
  'Authorization': f'Bearer {bearerToken}'
}


def downloadSubmissions(form_url: str, headers=headers) -> str:
    download_url = form_url + "submissions.csv.zip"
    form_file = f'odk_temp_download/{form_url.split("/")[-2]}.zip'
    params = {
        'attachments': False,
        '$filter': "__system/reviewState ne 'rejected' and __system/reviewState ne 'hasIssues'"
    }
    try:
        r = requests.get(download_url, headers=headers, stream=True, params=params)
        with open(form_file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        with zipfile.ZipFile(form_file, "r") as zip_ref:
            zip_ref.extractall(f"odk_temp_download/{form_url.split('/')[-2]}")
    except:
        print("Failed to download new")
        pass

    return f'odk_temp_download/{form_url.split("/")[-2]}'
