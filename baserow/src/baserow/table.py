import os
from typing import Callable, Iterable

class Table(object):
    def __init__(self, id: int, jwt_token: str) -> None:
        super().__init__()
        self.id = id
        self.jwt_token = jwt_token

    def get_rows(self, filter: Callable = None) -> Iterable:
        return []

def fetch(table_id) -> Table:
    return Table(table_id, os.environ['BASEROW_JWT'])
