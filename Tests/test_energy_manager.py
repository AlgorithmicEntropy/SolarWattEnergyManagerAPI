import logging
import os

from unittest import TestCase
from local_solar_watt import Api, DeviceClass


class TestEnergyManagerAPI(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._HOST = os.environ.get('ENERGY_MANAGER_HOST')

    def test_set_host(self):
        with self.assertRaises(ValueError):
            Api('')
        try:
            Api(self._HOST)
        except ValueError:
            self.fail('set_host() raised unexpected ValueError')

    def test_set_log_level(self):
        api = Api(self._HOST)
        try:
            api.set_log_level('WARNING')
        except ValueError:
            self.fail('set_log_level(str) raised unexpected ValueError')
        try:
            api.set_log_level(10)
        except ValueError:
            self.fail('set_log_level(int) raised unexpected ValueError')

    def test_set_logger(self):
        try:
            Api(self._HOST, logger=logging.Logger)
        except Exception as e:
            self.fail(f'unexpected exception: {repr(e)}')

    def test_test_connection(self):
        # this test only works if you own a compatible device (change host below)
        api = Api(self._HOST)
        try:
            status, data = api.test_connection()
            if not status:
                self.fail(f'Connection to energy manager failed, error: {data}')
        except Exception as e:
            self.fail(f'Unexpected exception: {repr(e)}')

    def test_pull_data(self):
        # this test only works if you own a compatible device (change host below)
        api = Api(self._HOST)
        api.set_log_level('DEBUG')
        try:
            result = api.pull_data()
            print(result)
        except Exception as e:
            self.fail(f'unexpected exception: {repr(e)}')
