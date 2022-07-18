from .api_client import ApiClient
import logging


class MyReserve(ApiClient):
    _API_PATH = '?topic=GetPerf&'
    _DEVICE_NAME = 'MyReserve'

    def test_connection(self):
        logging.info("Testing connection to energy manager")
        try:
            response = self._call_API()
            _ = response['SoC']
            if response:
                logging.info("Connected successfully to energy manager api")
                return True, response
            else:
                return False
        except TypeError:
            logging.error("Failed communication with api, no valid data returned")
            return False, "No valid data returned"

    def pull_data(self):
        data = self._call_API()
        result = {
            'soc': data['SoC'],
            'power_to_grid': data['PGrid'],
            'power_from_pv': data['PPV'],
            'power_from_bat': data['PBat'],
            'status.bms': data['BMSStatus'],
            'status.sys': data['SysStatus'],
            'status.com': data['ComStatus'],
            'status.inet': data['InternetStatus']
        }
        return result
