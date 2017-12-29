"""
Test EasyNido gear
"""
from unittest import TestCase

import os

# Test data in the same folder as this test
from yellowbot.datastoreservice import DatastoreService
from yellowbot.gears.easynidogear import EasyNidoGear

TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), "easynido_example_{}.txt")
DB_FILE_NAME = os.path.join(os.path.dirname(__file__), "test_db.json")

class TestEasyNidoGear(TestCase):
    def setUp(self):
        self._testdata1 = open(TESTDATA_FILENAME.format("5")).read()
        datastore = DatastoreService(DB_FILE_NAME)
        self._gear = EasyNidoGear(datastore)

    def tearDown(self):
        os.remove(DB_FILE_NAME)
        pass

    def test_parseData(self):
        assert 2 is self._gear.parse_webservice_data(self._testdata1)


