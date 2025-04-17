import logging

from local_solar_watt.clients import RestClient
from local_solar_watt.const import EnergyManagerVersion as EmV
from local_solar_watt.const import WorkUnits
from local_solar_watt.handlers import EmClassic
from local_solar_watt.handlers.flex import EmFlex

API_PATHS = {
    EmV.CLASSIC: "/rest/kiwigrid/wizard/devices",
    EmV.FLEX: "/rest/items"
}

DATA_PARSERS = {
    EmV.CLASSIC: EmClassic,
    EmV.FLEX: EmFlex
}


class EnergyManagerApi:
    def __init__(self, version: EmV, host: str, work_unit=WorkUnits.kWh, logger=None):
        self._logger = logger if logger else logging.getLogger(__name__)
        api_path = API_PATHS[version]
        self._client = RestClient(host, api_path, self._logger)
        self._handler = DATA_PARSERS[version](self._logger)
        self._version = version
        self._unit = work_unit

    def test_connection(self) -> bool:
        return self._client.test_connection()

    def fetch_data(self) -> dict:
        """
        Fetch data from the energy manager.
        """
        data = self._client.fetch_data_json()
        return self._handler.parse(data)
