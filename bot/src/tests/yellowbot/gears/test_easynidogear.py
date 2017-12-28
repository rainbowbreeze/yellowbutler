"""
Test EasyNido gear
"""
from unittest import TestCase

import os

# Test data in the same folder as this test
from yellowbot.gears.easynidogear import EasyNidoGear

TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), "easynido_example_{}.txt")


class TestEasyNidoGear(TestCase):
    def setUp(self):
        self._testdata1 = open(TESTDATA_FILENAME.format("1")).read()
        self._gear = EasyNidoGear()

    def tearDown(self):
        pass

    def test_parseData(self):
        assert None is self._gear.parse_webservice_data(self._testdata1)


