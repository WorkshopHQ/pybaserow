class BaserowConnect(object):
    def __init__(self, url: str) -> None:
        super().__init__()
        self.conn = {"url": url}

    def __enter__(self):
        # make a database connection and return it
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        # make sure the dbconnection gets closed
        print("Exit Baserow Connection")
