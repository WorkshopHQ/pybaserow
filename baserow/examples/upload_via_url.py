from pathlib import Path

from baserow.util import BaserowConnect
from baserow.table import fetch, upload_via_url

TABLE_ID = 288
BASEROW_URL = "http://baserow.hub/"

url = "http://baserow.hub/media/user_files/K3dxDdNv7TATEPI1YUX0PzDIBEsXwriO_368846f231c7661d00f36276a51113c92062fddb3383bb346029af60d02d079b.pdf"

with BaserowConnect(BASEROW_URL):
    table = fetch(TABLE_ID)
    remote_file = upload_via_url(url)
    data = {
        "Name": "upload from sdk via url",
        "Files": [{"name": remote_file}]
    }
    row_id = table.add_row(data)
    print(row_id)
