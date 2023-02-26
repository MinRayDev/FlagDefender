import json
from uuid import UUID

import requests

base_url = "http://127.0.0.1:5000/"


async def ping_server() -> bool:
    try:
        headers = {"Content-Type": "application/json"}
        response = requests.request("GET", base_url + "ping", headers=headers)
        print(response.text)
        return True
    except Exception as _:
        return False


async def get_party(party_id: str):
    try:
        headers = {"Content-Type": "application/json"}
        payload = {"party_id": party_id}
        response = requests.request("POST", base_url + "get_party", json=payload, headers=headers)
        return json.loads(response.text)
    except Exception as _:
        return None


async def get_party_by_code(code: int):
    try:
        headers = {"Content-Type": "application/json"}
        payload = {"code": code}
        response = requests.request("GET", base_url + "get_party", json=payload, headers=headers)
        return json.loads(response.text)
    except Exception as _:
        return None


async def create_party(user_id: UUID, client_id: UUID):
    try:
        headers = {"Content-Type": "application/json"}
        payload = {"user_id": str(user_id), "client_id": str(client_id)}
        response = requests.request("POST", base_url + "create_party", json=payload, headers=headers)
        return json.loads(response.text)
    except Exception as _:
        print("o")
        return None
