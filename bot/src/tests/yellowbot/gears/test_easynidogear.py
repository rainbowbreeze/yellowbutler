"""
Test EasyNido gear
"""
from unittest import TestCase

import os

# Test data in the same folder as this test
from yellowbot.datastoreservice import DatastoreService
from yellowbot.gears.easynidogear import EasyNidoGear

TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), "easynido_example_{}.txt")


class TestEasyNidoGear(TestCase):
    def setUp(self):
        self._testdata1 = open(TESTDATA_FILENAME.format("1")).read()
        self._gear = EasyNidoGear("username", "password", "idbambino")

    def tearDown(self):
        pass

    def test_parseData(self):
        # Uncomment to show parsing result, but test will fail
        #parsed = self._gear.parse_webservice_data(self._testdata1)
        #print(parsed)
        #assert 2 == 1
        pass


