from pathlib import Path

from baserow.util import BaserowConnect
from baserow.table import fetch, upload

TABLE_ID = 288
BASEROW_URL = "http://baserow.hub/"

file_path = Path("./file.pdf")

with BaserowConnect(BASEROW_URL):
    table = fetch(TABLE_ID)
    file_url = upload(file_path)
    print(file_url)
