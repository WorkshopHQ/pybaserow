import os
from typing import Dict, List
import requests
import json
import urllib

def login() -> str:
    # @TODO Add prompt if env variables are missing
    os.environ.setdefault("BASEROW_JWT", "")
    url = f"{os.environ['BASEROW_DOMAIN']}/api/user/token-auth/"
    res = requests.post(url, json={"username": os.environ['BASEROW_USERNAME'], "password": os.environ['BASEROW_PASSWORD']})
    user_token = json.loads(res.text)["token"]
    os.environ['BASEROW_JWT'] = user_token
    return user_token

def get_rows(table_id: int, get_all: bool = False) -> List[Dict]:
    url = f"{os.environ['BASEROW_DOMAIN']}/api/database/rows/table/{table_id}/?user_field_names=true"
    rows = []
    while True:
        res = requests.get(
            url,
            headers={
                "Authorization": f"JWT {os.environ['BASEROW_JWT']}"
            }
        )
        response = json.loads(res.content)
        rows.extend(response['results'])
        url = response['next']
        # no need for next page if not getting all rows or reaching the end
        if (not get_all) or (url is None):
            break
    return rows

def delete_row(table_id: int, row_id: int) -> None:
    requests.delete(
        f"http://baserow.hub/api/database/rows/table/{table_id}/{row_id}/",
        headers={
            "Authorization": f"JWT {os.environ['BASEROW_JWT']}"
        }
    )

def delete_rows(table_id: int, row_ids: List[int]) -> None:
    for row_id in row_ids:
        delete_row(table_id, row_id)


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