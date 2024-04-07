from abc import ABC, abstractmethod
import requests
import logging
import json


class ApiClient(ABC):
    _API_PATH = ''
    _DEVICE_NAME = ''
    _HEADERS = {'Accept': 'application/json'}
    _LOGGER = None

    def __init__(self, host: str, logger=None):
        if not host:
            raise ValueError('Invalid host')
        self._API_URL = "http://" + host + self._API_PATH
        if not logger:
            self._LOGGER = logging.getLogger(__name__)

    def set_log_level(self, log_level):
        if isinstance(log_level, str):
            numeric_level = getattr(logging, log_level.upper(), None)
            if not isinstance(numeric_level, int):
                raise ValueError('Invalid log level: %s' % log_level)
        if not (isinstance(log_level, int) or isinstance(log_level, str)):
            raise ValueError('Invalid log level: %s' % log_level)

        self._LOGGER.setLevel(log_level)

    def _call_api(self):
        try:
            response = requests.get(self._API_URL, headers=self._HEADERS)
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

    @abstractmethod
    def test_connection(self):
        pass

    @abstractmethod
    def pull_data(self):
        pass
