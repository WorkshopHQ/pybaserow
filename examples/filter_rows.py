from baserow.util import BaserowConnect
from baserow.table import fetch

table_id = 285

keys = set()
row_del_ids = []

with BaserowConnect("http://baserow.hub/"):
    table = fetch(table_id)
    rows = table.get_rows(get_all=True)
    for row in rows:
        row_key = row['Date'] + row['Url'] + row['Topic']
        if row_key in keys:
            row_del_ids.append(row['id'])
        keys.add(row_key)
    # delete duplicated rows
    table.del_rows(row_del_ids)
