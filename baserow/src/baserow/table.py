import os
import requests
import json
import logging
from typing import Callable, Iterable, List
from urllib.parse import urljoin
from pathlib import Path
from urllib.parse import urlparse

from tqdm import tqdm
import pandas as pd

logger = logging.getLogger(__name__)

class Table(object):
    def __init__(self, table_id: int, base_url: str, jwt_token: str) -> None:
        super().__init__()
        self.table_id = table_id
        self.base_url = base_url
        self.jwt_token = jwt_token

    def get_rows(self, filters: List[Callable] = [], get_all: bool = False, as_df: bool = False) -> Iterable:
        url = f"/api/database/rows/table/{self.table_id}/?user_field_names=true"
        url = urljoin(self.base_url, url)
        rows = []
        while True:
            res = requests.get(
                url,
                headers={
                    "Authorization": f"JWT {self.jwt_token}"
                }
            )
            response = json.loads(res.content)
            rows.extend(response['results'])
            url = response['next']
            print(f"[Baserow] Loaded {len(rows)} rows")
            # no need for next page if not getting all rows or reaching the end
            if (not get_all) or (url is None):
                break
        if as_df: # return as a dataframe
            rows = pd.DataFrame.from_dict(rows)
        return rows

    def del_row(self, row_id: int) -> None:
        url = f"/api/database/rows/table/{self.table_id}/{row_id}/"
        url = urljoin(self.base_url, url)
        requests.delete(
            url,
            headers={
                "Authorization": f"JWT {self.jwt_token}"
            }
        )

    def del_rows(self, row_ids: List[int]) -> None:
        for row_id in tqdm(row_ids):
            self.del_row(row_id)

    def add_row(self, row_data: dict) -> int:
        url = f"/api/database/rows/table/{self.table_id}/?user_field_names=true"
        url = urljoin(self.base_url, url)
        res = requests.post(
            url,
            headers={
                "Authorization": f"JWT {self.jwt_token}",
                "Content-Type": "application/json"
            },
            json=row_data
        )
        response = json.loads(res.content)
        return response["id"] if "id" in response else -1

    def add_rows(self, rows_data: List[dict]) -> List[int]:
        row_ids = []
        for row_data in rows_data:
            row_id = self.add_row(row_data)
            row_ids.append(row_id)
        return row_ids


def fetch(table_id: int) -> Table:
    return Table(table_id, os.environ['BASEROW_URL'], os.environ['BASEROW_JWT'])

# https://api.baserow.io/api/redoc/
def upload(file_path: Path) -> str:
    url = "/api/user-files/upload-file/"
    url = urljoin(os.environ['BASEROW_URL'], url)
    res = requests.post(
        url,
        headers={
            "Authorization": f"JWT {os.environ['BASEROW_JWT']}",
        },
        files={
            "file": open(file_path, 'rb')
        }
    )
    response = json.loads(res.content)
    return response["name"] if "name" in response else ""


def upload_via_url(file_url: str) -> str:
    url = "/api/user-files/upload-via-url/"
    url = urljoin(os.environ['BASEROW_URL'], url)
    res = requests.post(
        url,
        headers={
            "Authorization": f"JWT {os.environ['BASEROW_JWT']}",
            "Content-Type": "application/json"
        },
        json={
            "url": file_url
        }
    )
    response = json.loads(res.content)
    return response["name"] if "name" in response else ""
