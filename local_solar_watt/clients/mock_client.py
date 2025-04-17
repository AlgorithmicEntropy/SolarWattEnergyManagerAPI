import json

from local_solar_watt.base.base_client import BaseClient


class MockClient(BaseClient):
    def test_connection(self):
        return True

    def fetch_data_json(self):
        return self.json_data

    def __init__(self, json_path: str):
        self.json_path = json_path
        with open(json_path, 'r') as file:
            self.json_data = json.load(file)
