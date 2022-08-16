import os
from typing import Callable, Iterable, List
from urllib.parse import urljoin
import requests
import json
import logging

from tqdm import tqdm

logger = logging.getLogger(__name__)

class Table(object):
    def __init__(self, table_id: int, base_url: str, jwt_token: str) -> None:
        super().__init__()
        self.table_id = table_id
        self.base_url = base_url
        self.jwt_token = jwt_token

    def get_rows(self, filters: List[Callable] = [], get_all: bool = False) -> Iterable:
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
            print(f"Loaded {len(rows)} rows")
            # no need for next page if not getting all rows or reaching the end
            if (not get_all) or (url is None):
                break
        return rows

    def del_row(self, row_id: int) -> None:
        url = f"/api/database/rows/table/{self.table_id}/{row_id}/"
        url = urljoin(self.base_url, url)
        requests.delete(
            url,
            headers={
                "Authorization": f"JWT {os.environ['BASEROW_JWT']}"
            }
        )

    def del_rows(self, row_ids: List[int]) -> None:
        for row_id in tqdm(row_ids):
            self.del_row(row_id)


def fetch(table_id) -> Table:
    return Table(table_id, os.environ['BASEROW_URL'], os.environ['BASEROW_JWT'])
