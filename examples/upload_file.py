from pathlib import Path

from baserow.util import BaserowConnect
from baserow.table import fetch, upload

TABLE_ID = 288
BASEROW_URL = "http://baserow.hub/"

file_path = Path("./file.pdf")

with BaserowConnect(BASEROW_URL):
    table = fetch(TABLE_ID)
    remote_file = upload(file_path)
    data = {
        "Name": "upload from sdk",
        "Files": [{"name": remote_file}]
    }
    row_id = table.add_row(data)
    print(row_id)
