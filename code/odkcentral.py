import json
import os
from pathlib import Path
import requests
import sys
from tempfile import mkdtemp
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


def download_submissions(form_url: str, headers=headers) -> Optional[Path]:
    """
    Download and decompress the submission zipfile for a form.
    On success, returns the path to the folder with the CSV files.
    On error, returns None.
    """
    download_url = form_url + "submissions.csv.zip"
    
    base_name = form_url.split("/")[-2]
       
    # we use mkdtemp() instead of the newer TemporaryDirectory()
    # to prevent the temporary directory from being deleted
    # when TemporaryDirectory() falls out of scope.
    temp_dir = Path(mkdtemp())
    
    csv_zip_file = temp_dir / f'{base_name}.zip'
    data_dir = temp_dir / base_name
    
    if not temp_dir.exists():
        temp_dir.mkdir(exist_ok=True)

    if not data_dir.exists():
        data_dir.mkdir(exist_ok=True)

    params = {
        'attachments': False,
        '$filter': "__system/reviewState ne 'rejected' and __system/reviewState ne 'hasIssues'"
    }
    
    try:
        r = requests.get(download_url, headers=headers, stream=True, params=params)
        with open(csv_zip_file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        with zipfile.ZipFile(csv_zip_file, "r") as zip_ref:
            zip_ref.extractall(data_dir)
        csv_zip_file.unlink(missing_ok=True)
    except Exception as e:
        import traceback
        print(f"Failed to download file: {e}")
        traceback.print_exc()
        return None

    return data_dir
