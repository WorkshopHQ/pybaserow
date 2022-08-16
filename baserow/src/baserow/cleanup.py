from dotenv import load_dotenv

from baserow import login, get_rows, delete_row, delete_rows

load_dotenv()

token = login()

table_id = 285
row_ids = []
for row in get_rows(table_id, True):
    row_ids.append(row['id'])
print(row_ids)
delete_rows(table_id, row_ids)
