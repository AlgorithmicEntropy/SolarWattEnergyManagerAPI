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
            response = self._call_API()
            items = response['result']['items']
            if items:
                logging.info("Connected successfully to energy manager api")
                return True, response
            else:
                logging.error("Failed to connect with the energy manager api")
                logging.debug(f"HTTP Error code: {response.status_code}")
                return False
        except TypeError as e:
            logging.error("Failed communication with api, no valid data returned")
            return False, "No valid data returned"

        except Exception as e:
            logging.error("Failed to connect with the energy manager api")
            logging.debug(f"HTTP Error code: {repr(e)}")
            return False, repr(e)

    def pull_data(self):
        api_response = self._call_API()
        if api_response:
            # noinspection PyBroadException
            try:
                items = api_response['result']['items']
                # combine dicts into one with all relevant values
                all_items = {}
                for item in items:
                    for tag in item['tagValues']:
                        value = item['tagValues'][tag]['value']
                        all_items[tag] = value

                # power values in W
                # work in kWh
                return {
                    "energymanager.myreserve.charge": int(all_items['StateOfCharge']),
                    "energymanager.pv.power_produced": int(all_items['PowerProduced']),
                    "energymanager.sens.power_consumed": int(all_items['PowerConsumed']),
                    "energymanager.sens.power_consumed_grid": int(all_items['PowerConsumedFromGrid']),
                    "energymanager.sens.power_consumed_storage": int(all_items['PowerConsumedFromStorage']),
                    "energymanager.sens.power_consumed_producer": int(all_items['PowerConsumedFromProducers']),
                    "energymanager.sens.power_to_grid": int(all_items['PowerOut']),
                    "energymanager.myreserve.power_out": int(all_items['PowerOutFromStorage']),
                    "energymanager.myreserve.power_in": int(all_items['PowerBuffered']),
                    "energymanager.myreserve.power_self": int(all_items['PowerSelfSupplied']),
                    "energymanager.sens.power_self_consumed": int(all_items['PowerSelfConsumed']),
                    "energymanager.myreserve.power_in_grid": int(all_items['PowerBufferedFromGrid']),
                    "energymanager.myreserve.power_in_producers": int(all_items['PowerBufferedFromProducers']),
                    "energymanager.device.mode": all_items['ModeConverter'],
                    "energymanager.myreserve.health": float(all_items['StateOfHealth']),
                    "energymanager.myreserve.temperature": int(all_items['TemperatureBattery']),
                    "energymanager.device.load": float(all_items['FractionCPULoadAverageLastFiveMinutes']),
                    "energymanager.price.profit_feed": int(all_items["PriceProfitFeedin"]),
                    "energymanager.price.price_work_in": int(all_items["PriceWorkIn"]),
                    "energymanager.work.self_consumed": int(all_items["WorkSelfConsumed"]) // 1000,
                    "energymanager.work.self_supplied": int(all_items["WorkSelfSupplied"]) // 1000,
                    "energymanager.work.consumed": int(all_items["WorkConsumed"]) // 1000,
                    "energymanager.work.in": int(all_items["WorkIn"]) // 1000,
                    "energymanager.work.consumed_from_grid": int(all_items["WorkConsumedFromGrid"]) // 1000,
                    "energymanager.work.buffered_from_grid": int(all_items["WorkBufferedFromGrid"]) // 1000,
                    "energymanager.work.buffered_from_producers": int(all_items["WorkBufferedFromProducers"]) // 1000,
                    "energymanager.work.consumed_from_storage": int(all_items["WorkConsumedFromStorage"]) // 1000,
                    "energymanager.work.out_from_storage": int(all_items["WorkOutFromStorage"]) // 1000,
                    "energymanager.work.produced": int(all_items["WorkProduced"]) // 1000,
                    "energymanager.work.buffered": int(all_items["WorkBuffered"]) // 1000,
                    "energymanager.work.released": int(all_items["WorkReleased"]) // 1000,
                    "energymanager.work.out_from_producers": int(all_items["WorkOutFromProducers"]) // 1000,
                    "energymanager.work.consumed_from_producers": int(all_items["WorkConsumedFromProducers"]) // 1000,
                    "energymanager.work.out": int(all_items["WorkOut"]) // 1000,

                }
            except Exception as e:
                logging.error("Failed to parse energy manager data")
                logging.debug("Exception when parsing energy manager data: " + repr(e))
                return None
