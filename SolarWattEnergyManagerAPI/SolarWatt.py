import requests
import logging


class EnergyManagerAPI:
    API_PATH = "/rest/kiwigrid/wizard/devices"

    def __init__(self):
        self.API_URL = ""

    @staticmethod
    def set_log_level(log_level):
        if isinstance(log_level, str):
            numeric_level = getattr(logging, log_level.upper(), None)
            if not isinstance(numeric_level, int):
                raise ValueError('Invalid log level: %s' % log_level)
        if not (isinstance(log_level, int) or isinstance(log_level, str)):
            raise ValueError('Invalid log level: %s' % log_level)

        logging.basicConfig(level=log_level)

    def set_host(self, host: str):
        if not host:
            raise ValueError('Invalid host')
        self.API_URL = "http://" + host + self.API_PATH

    def _call_API(self):
        try:
            response = requests.get(self.API_URL)
            if response.status_code == 200:
                return response.json()
            else:
                logging.error("Failed to communicate with the energy manager API")
        except requests.exceptions.RequestException as e:
            logging.error("Failed to communicate with the energy manager API")
            logging.debug(f"HTTP Error code: {repr(e)}")

    def test_connection(self):
        logging.info("Testing connection to energy manager")
        try:
            response = requests.get(self.API_URL)
            if response.status_code == 200:
                logging.info("Connected successfully to energy manager api")
                return True
            else:
                logging.error("Failed to connect with the energy manager api")
                logging.debug(f"HTTP Error code: {response.status_code}")
                return False

        except requests.exceptions.RequestException as e:
            logging.error("Failed to connect with the energy manager api")
            logging.debug(f"HTTP Error code: {repr(e)}")
            return False

    def pull_data(self):
        api_response = self._call_API()
        if api_response:
            items = api_response['result']['items']
            # sort for consistency
            sorted(items, key=lambda element: element['guid'])
            # extract key sub components
            item_4_val = items[4]['tagValues']
            item_1_val = items[2]['tagValues']
            return {
                    "StateOfCharge": item_1_val['StateOfCharge']['value'],
                    "PowerProduced": item_4_val['PowerProduced']['value'],
                    "PowerConsumed": item_4_val['PowerConsumed']['value'],
                    "PowerConsumedFromGrid": item_4_val['PowerConsumedFromGrid']['value'],
                    "PowerConsumedFromStorage": item_4_val['PowerConsumedFromStorage']['value'],
                    "PowerConsumedFromProducers": item_4_val['PowerConsumedFromProducers']['value'],
                    "PowerOut": item_4_val['PowerOut']['value'],
                    "PowerOutFromStorage": item_4_val['PowerOutFromStorage']['value'],
                    "PowerBuffered": item_4_val['PowerBuffered']['value'],
                    "PowerSelfSupplied": item_4_val['PowerSelfSupplied']['value'],
                    "PowerSelfConsumed": item_4_val['PowerSelfConsumed']['value'],
                    "PowerReleased": item_4_val['PowerReleased']['value'],
                    "PowerBufferedFromGrid": item_4_val['PowerBufferedFromGrid']['value'],
                    "PowerBufferedFromProducers": item_4_val['PowerBufferedFromProducers']['value']
             }
