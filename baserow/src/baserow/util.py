import os
from typing import Dict
import requests
import json
from urllib.parse import urljoin

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
    return {
        "username": "",
        "password": ""
    }
