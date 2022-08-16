import os
from typing import Callable, Iterable, List
from urllib.parse import urljoin
import requests
import json

class Table(object):
    def __init__(self, id: int, base_url: str, jwt_token: str) -> None:
        super().__init__()
        self.id = id
        self.base_url = base_url
        self.jwt_token = jwt_token

    def get_rows(self, filters: List[Callable] = [], get_all: bool = False) -> Iterable:
        url = f"/api/database/rows/table/{self.id}/?user_field_names=true"
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
            # no need for next page if not getting all rows or reaching the end
            if (not get_all) or (url is None):
                break
        return rows

def fetch(table_id) -> Table:
    return Table(table_id, os.environ['BASEROW_URL'], os.environ['BASEROW_JWT'])
