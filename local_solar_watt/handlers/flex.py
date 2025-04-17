from local_solar_watt.base.base_handler import BaseHandler, EnergyData
from local_solar_watt.const import DeviceClass
from local_solar_watt.openhab import Item


class EmFlex(BaseHandler):
    """
    Data parser for the (old) style of the energy manager.
    """

    def __init__(self, logger=None):
        """
        Initialize the EnergyManager handler.
        :param logger: Optional logger instance.
        """
        super().__init__(logger)

    def _map_device_class(self, device: str) -> DeviceClass:
        """
        Map the device name to a defined device class.
        """
        if "battery" in device:
            return DeviceClass.BATTERY
        if "inverter" in device:
            return DeviceClass.INVERTER
        if "location" in device:
            return DeviceClass.LOCATION
        if "wallbox" in device:
            return DeviceClass.WALLBOX
        if "pvplant" in device:
            return DeviceClass.PV_PLANT
        if "meter" in device:
            return DeviceClass.METER
        else:
            self._logger.warning(f"Unknown device class for device: {device}")
            return DeviceClass.UNKNOWN

    def parse(self, d: dict) -> EnergyData:
        # parse into to list of items
        items = []
        for e in d:
            items.append(Item.from_json(e))
        # Get unique devices
        devices = set()
        for item in items:
            devices.add(f"{item.ha_entity.device}_{item.ha_entity.id}")
        # Group items by device
        grouped_items = {}
        for item in items:
            device = f"{item.ha_entity.device}_{item.ha_entity.id}"
            if device not in grouped_items:
                grouped_items[device] = []
            grouped_items[device].append(item)
        # map device classes
        mapped_devices = {}
        for device, items in grouped_items.items():
            mapped = self._map_device_class(items[0].ha_entity.device)
            if mapped not in mapped_devices:
                mapped_devices[mapped] = []
            mapped_devices[mapped].append(items)
        return mapped_devices
