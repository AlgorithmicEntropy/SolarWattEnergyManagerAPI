from unittest import TestCase

from local_solar_watt import DeviceClass
from local_solar_watt import EnergyManagerApi, EnergyManagerVersion, WorkUnits
from local_solar_watt.clients import MockClient
from local_solar_watt.handlers import EmClassic
from local_solar_watt.handlers.flex import EmFlex


class TestClassicApi(TestCase):
    def test_imports(self):
        api = EnergyManagerApi(EnergyManagerVersion.CLASSIC, "")
        api = EnergyManagerApi(EnergyManagerVersion.FLEX, "")
        api = EnergyManagerApi(EnergyManagerVersion.CLASSIC, "", work_unit=WorkUnits.Wh)

    # def test_online(self):
    #    api = EnergyManagerApi(EnergyManagerVersion.CLASSIC, "172.16.1.246")
    #    assert api.test_connection()
    #    data = api.fetch_data()
    #    assert data[DeviceClass.BATTERY][0]['device_state']

    def test_parsing_classic(self):
        client = MockClient('tests/data/energy_manager_classic.json')
        handler = EmClassic()
        parsed = handler.parse(client.fetch_data_json())
        assert parsed[DeviceClass.BATTERY_METER][0]['state_of_charge'] == 89

    def test_parsing_flex(self):
        client = MockClient('tests/data/energy_manager_flex.json')
        handler = EmFlex()
        parsed = handler.parse(client.fetch_data_json())
        assert len(parsed[DeviceClass.INVERTER]) == 3
        assert len(parsed[DeviceClass.PV_PLANT]) == 3
        assert len(parsed[DeviceClass.LOCATION]) == 1
        assert len(parsed[DeviceClass.LOCATION][0]) == 45
