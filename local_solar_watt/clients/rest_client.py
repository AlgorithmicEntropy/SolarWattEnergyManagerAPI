import json
import logging

import requests

from local_solar_watt.base.base_client import BaseClient

_HEADERS = {'Accept': 'application/json'}


class RestClient(BaseClient):
    _DEVICE_NAME = 'energyManager'

    def __init__(self, host: str, api_path: str, logger=None):
        self._host = host
        self._path = api_path
        self._url = "http://" + host + self._path
        if not logger:
            self._logger = logging.getLogger(__name__)

    def set_log_level(self, log_level):
        if isinstance(log_level, str):
            numeric_level = getattr(logging, log_level.upper(), None)
            if not isinstance(numeric_level, int):
                raise ValueError('Invalid log level: %s' % log_level)
        if not (isinstance(log_level, int) or isinstance(log_level, str)):
            raise ValueError('Invalid log level: %s' % log_level)

        self._logger.setLevel(log_level)

    def fetch_data_json(self):
        try:
            response = requests.get(self._url, headers=_HEADERS)
            if response.status_code == 200:
                return response.json()
            else:
                logging.error(f"Failed to communicate with the {self._DEVICE_NAME} API")
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to communicate with {self._DEVICE_NAME} API")
            logging.debug(f"HTTP Error code: {repr(e)}")
        except json.decoder.JSONDecodeError as e:
            logging.error(f"Failed to communicate with the {self._DEVICE_NAME} API")
            logging.debug(f"JSON decode error: {repr(e)}")
        return None

    def test_connection(self):
        logging.info("Testing connection to energy manager")
        try:
            response = self.fetch_data_json()
            items = response['result']['items']
            if items:
                logging.info("Connected successfully to energy manager api")
                return True
            else:
                return False
        except TypeError:
            logging.error("Failed communication with api, no valid data returned")
            return False, "No valid data returned"

        except Exception as e:
            logging.error("Failed to connect with the energy manager api")
            logging.debug(f"HTTP Error code: {repr(e)}")
            return False
