import os
from typing import Dict, Union
import requests
import json
from pathlib import Path
from urllib.parse import urljoin

from rich.prompt import Prompt

class BaserowConnect(object):
    def __init__(self, url: str, cert: Union[Dict, None] = None) -> None:
        super().__init__()
        self.url = url
        self.cert = cert
        self.prev_jwt = ""
        self.prev_url = ""

    def __enter__(self) -> None:
        self.prev_jwt = os.environ.get("BASEROW_JWT", "")
        self.prev_url = os.environ.get("BASEROW_URL", "")
        url = urljoin(self.url, "/api/user/token-auth/")
        cert = self.cert if self.cert else load_cert()
        res = requests.post(url, json=cert)
        if res.status_code != 201:
            raise Exception(f"Failed to authenticate baserow")
        user_token = json.loads(res.text)["token"]
        os.environ["BASEROW_JWT"] = user_token
        os.environ["BASEROW_URL"] = self.url

    def __exit__(self, exc_type, exc_val, exc_tb):
        # reset global environment on exit
        os.environ.setdefault("BASEROW_JWT", self.prev_jwt)
        os.environ.setdefault("BASEROW_URL", self.prev_url)

def load_cert() -> Dict:
    config_dir = Path(Path.home(), ".baserow")
    if not config_dir.exists():
        os.makedirs(config_dir)
    # load certificate file
    cert_path = Path(config_dir, "cert.json")
    if not cert_path.exists():
        username = Prompt.ask("Username")
        password = Prompt.ask("Password")
        with open(cert_path, "w+") as f:
            json.dump({"username": username, "password": password}, f)
    with open(cert_path) as f:
        return json.load(f)
