import os
from typing import Callable

class Table(object):
    def __init__(self, id: int) -> None:
        super().__init__()
        self.id = id

    def get_rows(self, filter: Callable = None):
        return []

def fetch(table_id) -> Table:
    print(f"table id {table_id}")
    print(os.environ['BASEROW_JWT'])
    return Table(table_id)
