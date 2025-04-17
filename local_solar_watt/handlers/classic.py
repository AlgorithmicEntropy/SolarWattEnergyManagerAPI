from local_solar_watt.base.base_handler import BaseHandler, EnergyData, ParsingError
from local_solar_watt.const import TAGS_CLASSIC, DeviceClass, Device, WorkUnits


class EmClassic(BaseHandler):
    """
    Data parser for the (old) style of the energy manager.
    """

    def __init__(self, logger=None):
        """
        Initialize the EnergyManager handler.
        :param logger: Optional logger instance.
        """
        super().__init__(logger)

    def parse(self, d: dict) -> EnergyData:
        # noinspection PyBroadException
        try:
            devices = d['result']['items']
            d = self._parse_devices(devices)

            # Find devices in the returned data
            data = {}
            for device in d:
                if DeviceClass.BATTERY_METER.value in device.tags:
                    data[DeviceClass.BATTERY_METER] = self._extract_values(device,
                                                                           TAGS_CLASSIC[DeviceClass.BATTERY_METER])
                elif DeviceClass.BATTERY.value in device.tags:
                    data[DeviceClass.BATTERY] = self._extract_values(device, TAGS_CLASSIC[DeviceClass.BATTERY])
                elif DeviceClass.INVERTER.value in device.tags and DeviceClass.BATTERY_METER.value not in device.tags:
                    data[DeviceClass.INVERTER] = self._extract_values(device, TAGS_CLASSIC[DeviceClass.INVERTER])
                elif DeviceClass.LOCATION.value in device.tags:
                    data[DeviceClass.LOCATION] = self._extract_values(device, TAGS_CLASSIC[DeviceClass.LOCATION])

            return data

        except Exception as e:
            self._logger.error("Failed to parse energy manager data")
            self._logger.debug("Exception when parsing energy manager data: " + repr(e))
            raise ParsingError("Failed to parse energy manager data") from e

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
            try:
                # change power values to kWh if applicable
                if 'work' in key and self._work_unit == WorkUnits.kWh:
                    value = device.values[val]
                    if value:
                        value = value / 1000
                    data[key] = value
                else:
                    data[key] = device.values[val]
            except KeyError:
                self._logger.error(f"Failed to extract data value for {key}")
        # returning a list is just a lazy fix, as the code cant actually handle more than one device per class
        return [data]
