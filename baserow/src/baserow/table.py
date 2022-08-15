from abc import ABC

class Table(ABC):
    def __init__(self) -> None:
        super().__init__()

def fetch(table_id) -> Table:
    return Table()
