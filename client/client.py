#!/usr/bin/env python3
import time
import requests


class FlexStoreClient:
    def __init__(self, gateway_url: str):
        self.gateway_url = gateway_url

    def get(self, key: str):
        try:
            response = requests.get(f"{self.gateway_url}/kv/{key}")
            if response.status_code == 404:
                return None
            return response.json().get("value")
        except Exception as e:
            return f"Something went wrong: {str(e)}"

    def put(self, key: str, value: str):
        try:
            response = requests.put(f"{self.gateway_url}/kv/{key}", data=value)
            return response.json()
        except Exception as e:
            return f"Something went wrong: {str(e)}"

    def delete(self, key: str):
        try:
            response = requests.delete(f"{self.gateway_url}/kv/{key}")
            return response.status_code == 200
        except Exception as e:
            return f"Something went wrong: {str(e)}"


if __name__ == "__main__":
    fs_client = FlexStoreClient("http://localhost:8002")

    key_values = {
        "alpha": "alpha",
        "bravo": "bravo",
        "charlie": "delta",
        "echo": "echo",
        "foxtrot": "foxtrot",
        "golf": "golf",
        "hotel": "hotel",
        "india": "india",
        "juliet": "juliet"
    }

    for key, value in key_values.items():
        print(f"Sarting to put key={key}, value={value}")
        fs_client.put(key, value)
        print(f"Done")
        time.sleep(1.0)