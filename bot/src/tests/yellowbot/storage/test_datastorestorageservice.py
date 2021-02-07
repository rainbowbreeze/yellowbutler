"""Test Firestore in Datastore more storage service
"""

from unittest import TestCase

import os
import datetime

from yellowbot.storage.datastorestorageservice import DatastoreStorageService, BaseEntity

class DummyEntity(BaseEntity):
    """Entity to store information during this test
    """
    url: str
    last_check: datetime.date

    def __init__(self) -> None:
        """
        """
        super().__init__()  # Sets fundamental entity properties
        self.url: None
        self.last_check: None

    @staticmethod
    def get_entity_name() -> str:
        return __class__.__name__

    def to_dict(self) -> dict:
        fields = {}
        if hasattr(self, "url"):
            fields["url"] = self.url
        if hasattr(self, "last_check"):
            fields["last_check"] = self.last_check
        return fields

    def from_dict(self, source_dict: dict):
        if hasattr(source_dict, "url"):
            self.url = source_dict["url"]
        if hasattr(source_dict, "last_check"):
            self.last_check = source_dict["last_check"]
        return self


class TestDatastoreStorageService(TestCase):
    def setUp(self):
        self._datastore = DatastoreStorageService()
        pass

    def tearDown(self):
        # TODO clean-up the datastore for the specific entity used during this test
        pass

    def test_write_and_read(self):
        test_item = DummyEntity()
        timenow = datetime.datetime.now()
        test_item.url = "testing_url_{}".format(timenow)
        test_item.last_check = timenow

        entity_id = self._datastore.put(test_item)
        self.assertIsNotNone(entity_id)
        self.assertEqual(entity_id, test_item.id)

        test_items = self._datastore.query_all(DummyEntity.get_entity_name(), DummyEntity)
        self.assertEqual(1, len(test_items))

        self._datastore.delete_all(DummyEntity.get_entity_name())
        test_items = self._datastore.query_all(DummyEntity.get_entity_name(), DummyEntity)
        self.assertEqual(0, len(test_items))

        #test_item = self._datastore.query_from_id()



