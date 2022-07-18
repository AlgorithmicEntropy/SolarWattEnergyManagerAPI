import requests
import logging
import json

from .api_client import ApiClient
from LocalSolarWatt.units import WorkUnits


class EnergyManagerApi(ApiClient):
    _API_PATH = "/rest/kiwigrid/wizard/devices"
    _DEVICE_NAME = 'energy manager'

    def __init__(self, host: str, work_unit=WorkUnits.kWh, logger=None):
        super().__init__(host, logger)
        self._unit = work_unit

    def test_connection(self):
        logging.info("Testing connection to energy manager")
        try:
            response = self._call_API()
            items = response['result']['items']
            if items:
                logging.info("Connected successfully to energy manager api")
                return True, response
            else:
                return False
        except TypeError:
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
                result = {
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
                    "energymanager.price.profit_feed": int(all_items["PriceProfitFeedin"]) / 100,
                    "energymanager.price.price_work_in": int(all_items["PriceWorkIn"]) / 100,
                    "energymanager.work.self_consumed": int(all_items["WorkSelfConsumed"]),
                    "energymanager.work.self_supplied": int(all_items["WorkSelfSupplied"]),
                    "energymanager.work.consumed": int(all_items["WorkConsumed"]),
                    "energymanager.work.in": int(all_items["WorkIn"]),
                    "energymanager.work.consumed_from_grid": int(all_items["WorkConsumedFromGrid"]),
                    "energymanager.work.buffered_from_grid": int(all_items["WorkBufferedFromGrid"]),
                    "energymanager.work.buffered_from_producers": int(all_items["WorkBufferedFromProducers"]),
                    "energymanager.work.consumed_from_storage": int(all_items["WorkConsumedFromStorage"]),
                    "energymanager.work.out_from_storage": int(all_items["WorkOutFromStorage"]),
                    "energymanager.work.produced": int(all_items["WorkProduced"]),
                    "energymanager.work.buffered": int(all_items["WorkBuffered"]),
                    "energymanager.work.released": int(all_items["WorkReleased"]),
                    "energymanager.work.out_from_producers": int(all_items["WorkOutFromProducers"]),
                    "energymanager.work.consumed_from_producers": int(all_items["WorkConsumedFromProducers"]),
                    "energymanager.work.out": int(all_items["WorkOut"]),
                }

                # change power values to kWh if applicable
                if self._unit == WorkUnits.kWh:
                    for key in result:
                        if 'energymanager.work' in key:
                            result[key] = result[key] / 1000

                return result

            except Exception as e:
                logging.error("Failed to parse energy manager data")
                logging.debug("Exception when parsing energy manager data: " + repr(e))
                return None
