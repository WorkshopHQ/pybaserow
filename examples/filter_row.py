from baserow import auth, table

with auth.login("http://baserow.hub/"):
    def is_dataops_row(row):
        return "Topic" in row and row["Topic"] == "dataops"

    table_id = 285
    table_data = table.fetch(table_id)
    dataops_rows = table_data.get_rows(is_dataops_row)
