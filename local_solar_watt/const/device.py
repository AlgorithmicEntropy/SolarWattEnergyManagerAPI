from dataclasses import dataclass
from enum import Enum


class EnergyManagerVersion(Enum):
    """Enum for the energy manager version"""
    CLASSIC = "classic"
    FLEX = "flex"


class DeviceClass(Enum):
    BATTERY = "PowerMeter"
    BATTERY_METER = "BatteryConverter"
    INVERTER = "Inverter"
    LOCATION = "Location"
    WALLBOX = "Wallbox"
    PV_PLANT = "PVPlant"
    METER = "Meter"
    UNKNOWN = "Unknown"


@dataclass
class Device:
    """Represents a device connected to the energy manager"""
    tags: list[str]
    values: dict
