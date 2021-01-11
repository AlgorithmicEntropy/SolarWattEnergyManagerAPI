import requests
import logging
import json


class EnergyManagerAPI:
    _API_PATH = "/rest/kiwigrid/wizard/devices"
    _HEADERS = {'Accept': 'application/json'}
    _LOGGER = None

    def __init__(self):
        self._API_URL = ""
        self._LOGGER = logging.getLogger(__name__)

    def set_log_level(self, log_level):
        if isinstance(log_level, str):
            numeric_level = getattr(logging, log_level.upper(), None)
            if not isinstance(numeric_level, int):
                raise ValueError('Invalid log level: %s' % log_level)
        if not (isinstance(log_level, int) or isinstance(log_level, str)):
            raise ValueError('Invalid log level: %s' % log_level)

        self._LOGGER.setLevel(log_level)

    def set_logger(self, logger):
        self._LOGGER = logger

    def set_host(self, host: str):
        if not host:
            raise ValueError('Invalid host')
        self._API_URL = "http://" + host + self._API_PATH

    def _call_API(self):
        try:
            response = requests.get(self._API_URL, headers=self._HEADERS)
            if response.status_code == 200:
                return response.json()
            else:
                logging.error("Failed to communicate with the energy manager API")
        except requests.exceptions.RequestException as e:
            logging.error("Failed to communicate with the energy manager API")
            logging.debug(f"HTTP Error code: {repr(e)}")
        except json.decoder.JSONDecodeError as e:
            logging.error("Failed to communicate with the energy manager API")
            logging.debug(f"JSON decode error: {repr(e)}")
        return None

    def test_connection(self):
        logging.info("Testing connection to energy manager")
        try:
            response = requests.get(self._API_URL, headers=self._HEADERS)
            if response.status_code == 200:
                # try decode info
                response.json()
                logging.info("Connected successfully to energy manager api")
                return True
            else:
                logging.error("Failed to connect with the energy manager api")
                logging.debug(f"HTTP Error code: {response.status_code}")
                return False

        except (requests.exceptions.RequestException, json.decoder.JSONDecodeError) as e:
            logging.error("Failed to connect with the energy manager api")
            logging.debug(f"HTTP Error code: {repr(e)}")
            return False

    def pull_data(self):
        api_response = self._call_API()
        if api_response:
            items = api_response['result']['items']
            # sort for consistency
            items = sorted(items, key=lambda element: element['guid'])
            # extract key sub components
            item_4_val = items[4]['tagValues']
            item_1_val = items[1]['tagValues']
            return {
                    "energymanager.myreserve.charge": item_1_val['StateOfCharge']['value'],
                    "energymanager.pv.power_produced": item_4_val['PowerProduced']['value'],
                    "energymanager.sens.power_consumed": item_4_val['PowerConsumed']['value'],
                    "energymanager.sens.power_consumed_grid": item_4_val['PowerConsumedFromGrid']['value'],
                    "energymanager.sens.power_consumed_storage": item_4_val['PowerConsumedFromStorage']['value'],
                    "energymanager.sens.power_consumed_producer": item_4_val['PowerConsumedFromProducers']['value'],
                    "energymanager.sens.power_to_grid": item_4_val['PowerOut']['value'],
                    "energymanager.myreserve.power_out": item_4_val['PowerOutFromStorage']['value'],
                    "energymanager.myreserve.power_in": item_4_val['PowerBuffered']['value'],
                    "energymanager.myreserve.power_self": item_4_val['PowerSelfSupplied']['value'],
                    "energymanager.sens.power_self_consumed": item_4_val['PowerSelfConsumed']['value'],
                    # "PowerReleased": item_4_val['PowerReleased']['value'], --> need to figure out meaning
                    "energymanager.myreserve.power_in_grid": item_4_val['PowerBufferedFromGrid']['value'],
                    "energymanager.myreserve.power_in_producers": item_4_val['PowerBufferedFromProducers']['value']
             }
