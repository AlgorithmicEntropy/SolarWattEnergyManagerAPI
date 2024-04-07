import logging

from .api_client import ApiClient
from local_solar_watt.units import WorkUnits
from .device import Device, DeviceClass
import local_solar_watt.tags as tags


class EnergyManagerApi(ApiClient):
    _API_PATH = "/rest/kiwigrid/wizard/devices"

    def __init__(self, host: str, work_unit=WorkUnits.kWh, logger=None):
        super().__init__(host, logger)
        self._unit = work_unit

    def test_connection(self):
        logging.info("Testing connection to energy manager")
        try:
            response = self._call_api()
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

    @staticmethod
    def _parse_devices(device_list):
        """Extract relevant data and connected device types from api payload"""
        parsed_devices = []
        for d in device_list:
            device_tags = [t['deviceClass'].split('.')[-1] for t in d['deviceModel']]
            tag_values = {}
            for tag in d['tagValues']:
                tag_values[tag] = d['tagValues'][tag]['value']
            device = Device(tags=device_tags, values=tag_values)
            parsed_devices.append(device)
        return parsed_devices

    def _extract_values(self, device: Device, fields: dict):
        """Extract relevant values from device"""
        data = {}
        for key, val in fields.items():
            # change power values to kWh if applicable
            if 'work' in key and self._unit == WorkUnits.kWh:
                value = device.values[val]
                if value:
                    value = value / 1000
                data[key] = value
            else:
                data[key] = device.values[val]
        return data

    def pull_data(self):
        api_response = self._call_api()
        if api_response:
            # noinspection PyBroadException
            try:
                devices = api_response['result']['items']
                d = self._parse_devices(devices)

                # Find devices in the returned data
                data = {}
                for device in d:
                    if DeviceClass.BATTERY_METER.value in device.tags:
                        data[DeviceClass.BATTERY_METER] = self._extract_values(device, tags.BATTERY_METER)
                    elif DeviceClass.BATTERY.value in device.tags:
                        data[DeviceClass.BATTERY] = self._extract_values(device, tags.BATTERY)
                    elif DeviceClass.INVERTER.value in device.tags and DeviceClass.BATTERY_METER.value not in device.tags:
                        data[DeviceClass.INVERTER] = self._extract_values(device, tags.INVERTER)
                    elif DeviceClass.LOCATION.value in device.tags:
                        data[DeviceClass.LOCATION] = self._extract_values(device, tags.LOCATION)

                return data

            except Exception as e:
                logging.error("Failed to parse energy manager data")
                logging.debug("Exception when parsing energy manager data: " + repr(e))
                if __debug__:
                    raise e
                return None

    def pull_raw(self):
        return self._call_api()
