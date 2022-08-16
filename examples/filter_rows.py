from baserow.util import BaserowConnect
from baserow.table import fetch

def is_dataops_row(row):
    return "Topic" in row and row["Topic"] == "dataops"

table_id = 285

with BaserowConnect("http://baserow.hub/"):
    table = fetch(table_id)
    rows = table.get_rows(get_all=True)
    print(len(rows))
