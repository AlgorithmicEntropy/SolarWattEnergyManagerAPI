import logging
from abc import ABC, abstractmethod

from local_solar_watt.const import DeviceClass, WorkUnits

type EnergyData = dict[DeviceClass, list[dict[str, any]]]


class ParsingError(Exception):
    """
    Custom exception for data parsing errors.
    """

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class BaseHandler(ABC):
    """
    Base class for data parsing from different api clients.
    """

    def __init__(self, work_unit=WorkUnits.kWh, logger=None):
        """
        Initialize the data handler.
        :param work_unit: The work unit to use.
        """
        self._work_unit = work_unit
        if not logger:
            self._logger = logging.getLogger(__name__)

    @abstractmethod
    def parse(self, d: dict) -> EnergyData:
        """
        Parse the json data from the API client.
        :return: Parsed data.
        """
        pass
