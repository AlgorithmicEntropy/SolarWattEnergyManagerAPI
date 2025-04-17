from collections import defaultdict
from typing import Dict, List

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

    def parse(self, raw_items: dict) -> EnergyData:
        # Deserialize and build per‑device dicts
        grouped: Dict[str, Dict[str, Item]] = defaultdict(dict)
        for raw in raw_items:
            item = Item.from_json(raw)
            # device bucket for all entities belonging to the same device+id
            device_key = f"{item.ha_entity.device}_{item.ha_entity.id}"
            # unique key for each individual entity/item
            item_key = f"{item.ha_entity.device}_{item.ha_entity.id}_{item.ha_entity.entity}"
            grouped[device_key][item_key] = item

        # Bucket device dicts by *mapped* device class
        mapped_devices: Dict[DeviceClass, List[Dict[str, Item]]] = defaultdict(list)
        for device_dict in grouped.values():
            # Peek at any item to discover the mapping key for this whole device
            any_item = next(iter(device_dict.values()))
            mapped_key = self._map_device_class(any_item.ha_entity.device)
            mapped_devices[mapped_key].append(device_dict)
        return mapped_devices
