"""Test Firestore in Datastore more storage service
"""

from unittest import TestCase

import os
import datetime

from yellowbot.storage.datastorestorageservice import DatastoreStorageService
from yellowbot.storage.newsitementity import NewsItemEntity


class TestDatastoreStorageService(TestCase):
    def setUp(self):
        self._service = DatastoreStorageService()
        pass

    def tearDown(self):
        pass

    def test_write_and_read(self):
        news_item = NewsItemEntity()
        news_item.url = "testing_url_"
        news_item.last_check = datetime.datetime.now()
        id = self._service.put(news_item)
        self.assertIsNotNone(id)


