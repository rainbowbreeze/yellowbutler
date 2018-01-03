"""
Test datastore service
"""

from unittest import TestCase

import os

from yellowbot.datastoreservice import DatastoreService

DB_FILE_NAME = os.path.join(os.path.dirname(__file__), "test_db.json")


class TestDatastoreService(TestCase):
    def setUp(self):
        self._service = DatastoreService(DB_FILE_NAME)
        pass

    def tearDown(self):
        os.remove(DB_FILE_NAME)
        pass

    def test_write_and_read(self):
        self._service.write({
                'key1': "key1_value",
                'key2': 3,
                'key3': "long text string"
            })

        query = self._service.create_query()
        result = self._service.search(query.key1 == "key1_value")
        assert 3 == result[0]["key2"]
        assert "long text string" == result[0]["key3"]

