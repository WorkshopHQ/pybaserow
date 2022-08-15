from baserow.util import BaserowConnect
from baserow.table import fetch


with BaserowConnect("http://baserow.hub/"):
    def is_dataops_row(row):
        return "Topic" in row and row["Topic"] == "dataops"

    table_id = 285
    table = fetch(table_id)
    dataops_rows = table.get_rows(is_dataops_row)
