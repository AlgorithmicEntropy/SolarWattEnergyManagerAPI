import os

from LocalSolarWatt import MyReserve
from unittest import TestCase


class TestMyReserve(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._HOST = os.environ.get('MY_RESERVE_HOST')

    def test_pull_data(self):
        api = MyReserve(self._HOST)
        status, data = api.test_connection()
        self.assertTrue(status)
        print(data)