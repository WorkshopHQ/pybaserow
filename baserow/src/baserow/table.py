import os
from typing import Callable, Iterable

class Table(object):
    def __init__(self, id: int, url: str, jwt_token: str) -> None:
        super().__init__()
        self.id = id
        self.url = url
        self.jwt_token = jwt_token

    def get_rows(self, filter: Callable = None) -> Iterable:
        return []

def fetch(table_id) -> Table:
    return Table(table_id, os.environ['BASEROW_URL'], os.environ['BASEROW_JWT'])
