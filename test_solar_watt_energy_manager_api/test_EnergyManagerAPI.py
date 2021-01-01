from unittest import TestCase
import solar_watt_energy_manager_api as api


class TestEnergyManagerAPI(TestCase):
    def test_EnergyManagerAPI(self):
        with self.assertRaises(ValueError):
            api.EnergyManagerAPI('')
        with self.assertRaises(ValueError):
            api.EnergyManagerAPI('hostname', 'INVALID_LOG_LEVEL')
        try:
            api.EnergyManagerAPI('hostname', 'INFO')
        except ValueError:
            self.fail('ctor raised unexpected ValueError')

    def test_test_connection(self):
        energy_manager_api = api.EnergyManagerAPI('172.16.1.246')
        try:
            energy_manager_api.test_connection()
        except Exception as e:
            self.fail(f'unexpected exception: {repr(e)}')

    def test_pull_data(self):
        energy_manager_api = api.EnergyManagerAPI('172.16.1.246')
        try:
            result = energy_manager_api.pull_data()
            # print(result)
        except Exception as e:
            self.fail(f'unexpected exception: {repr(e)}')
