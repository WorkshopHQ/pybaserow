import os
from typing import Dict, List
import requests
import json
import urllib

def download_file(url: str, file_name: str, output_dir: str = None) -> str:
    if output_dir is None:
        output_dir = os.getcwd()
    file_path = os.path.join(output_dir, file_name)
    urllib.request.urlretrieve(url, file_path)

def create_row(domain_url: str, table_id: int, data: Dict, token: str):
    url = f"{domain_url}/api/database/rows/table/{table_id}/?user_field_names=true"
    requests.post(
        url,
        headers={
            "Authorization": f"JWT {token}",
            "Content-Type": "application/json"
        },
        json=data
    )

def upload_file(domain_url: str, file_path: str, token: str):
    url = f"{domain_url}/api/user-files/upload-file/"
    with open(file_path, "rb") as file:
        file_dict = {"file": file}
        response = requests.post(
            url,
            headers={
                "Authorization": f"JWT {token}",
            },
            files=file_dict
        )
    file_name = json.loads(response.text)["name"]
    return file_name
