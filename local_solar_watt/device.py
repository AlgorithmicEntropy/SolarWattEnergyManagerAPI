from dataclasses import dataclass
from enum import Enum


class DeviceClass(Enum):
    BATTERY = "PowerMeter"
    BATTERY_METER = "BatteryConverter"
    INVERTER = "Inverter"
    LOCATION = "Location"


@dataclass
class Device:
    """Represents a device connected to the energy manager"""
    tags: list[str]
    values: dict
