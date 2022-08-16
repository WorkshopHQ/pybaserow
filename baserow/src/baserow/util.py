import os
from typing import Dict
import requests
import json
from pathlib import Path
from urllib.parse import urljoin

from rich.prompt import Prompt

class BaserowConnect(object):
    def __init__(self, url: str) -> None:
        super().__init__()
        self.base_url = url

    def __enter__(self) -> None:
        os.environ.setdefault("BASEROW_JWT", "")
        url = urljoin(self.base_url, "/api/user/token-auth/")
        res = requests.post(url, json=load_cert())
        if res.status_code != 201:
            raise Exception(f"Failed to authenticate baserow")
        user_token = json.loads(res.text)["token"]
        os.environ['BASEROW_JWT'] = user_token

    def __exit__(self, exc_type, exc_val, exc_tb):
        # reset BASEROW_JWT for safety
        os.environ.setdefault("BASEROW_JWT", "")

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
