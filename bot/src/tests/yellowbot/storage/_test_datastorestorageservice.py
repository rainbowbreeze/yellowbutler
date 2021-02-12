"""Test Firestore in Datastore more storage service
"""

from typing import Any, Dict
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
        return "DummyEntity"

    def to_dict(self) -> Dict[str, Any]:
        fields: Dict[str, Any] = {}
        if hasattr(self, "url"):
            fields["url"] = self.url
        if hasattr(self, "last_check"):
            fields["last_check"] = self.last_check
        return fields

    def from_dict(self, source_dict: dict):
        if "url" in source_dict:
            self.url = source_dict["url"]
        if "last_check" in source_dict:
            self.last_check = source_dict["last_check"]
        return self


class TestDatastoreStorageService(TestCase):
    def setUp(self):
        self._datastore = DatastoreStorageService()
        pass

    def tearDown(self):
        self._datastore.delete_all(DummyEntity)

    def test_delete_all(self):
        # Check for errors if no entities are stored
        self._datastore.delete_all(DummyEntity)
        self._datastore.delete_all(DummyEntity)

    def test_name(self):
        nameclass = DummyEntity
        self.assertEqual(DummyEntity.get_entity_name(), nameclass.get_entity_name())

    def test_write_and_read(self):
        # ---- Tests for adding new entities to the datastore ----
        # Add entity 1 to the datastore
        test_entity1 = self._create_dummy_entity()
        entity_id1 = self._datastore.put(test_entity1)
        self.assertIsNotNone(entity_id1)
        self.assertEqual(entity_id1, test_entity1.id)

        read_entities = self._datastore.get_all(DummyEntity)
        self.assertEqual(1, len(read_entities))
        self.assertEqual(test_entity1.id, read_entities[0].id)
        self.assertEqual(test_entity1.url, read_entities[0].url)
        # Checks timestamp() because the returned object from Datastore is a DatetimeWithNanoseconds
        # self.assertEqual(test_entity1.last_check.timestamp(), test_items[0].last_check.timestamp())

        # Add entity 2 to the datastore
        test_entity2 = self._create_dummy_entity()
        entity_id2 = self._datastore.put(test_entity2)
        self.assertIsNotNone(entity_id2)
        self.assertEqual(entity_id2, test_entity2.id)
        # And check total database elements
        read_entities = self._datastore.get_all(DummyEntity)
        self.assertEqual(2, len(read_entities))

        # Add entity 3 to the datastore
        test_entity3 = self._create_dummy_entity()
        entity_id3 = self._datastore.put(test_entity3)
        self.assertIsNotNone(entity_id3)
        self.assertEqual(entity_id3, test_entity3.id)
        # And check total database elements
        read_entities = self._datastore.get_all(DummyEntity)
        self.assertEqual(3, len(read_entities))


        # ---- Tests for retrieving entities from the datastore using keys ----
        # Get entity 2 by id
        read_entity = self._datastore.get_by_id(DummyEntity, entity_id2)
        self.assertIsNotNone(read_entity)
        self.assertEqual(test_entity2.id, read_entity.id)
        self.assertEqual(test_entity2.url, read_entity.url)
        #self.assertEqual(test_entity2.last_check.timestamp(), read_entity.last_check.timestamp())

        # Get entity 3 by id
        read_entity = self._datastore.get_by_id(DummyEntity, entity_id3)
        self.assertIsNotNone(read_entity)
        self.assertEqual(test_entity3.id, read_entity.id)
        self.assertEqual(test_entity3.url, read_entity.url)
        #self.assertEqual(test_entity3.last_check.timestamp(), read_entity.last_check.timestamp())

        # Get entity 1 by id
        read_entity = self._datastore.get_by_id(DummyEntity, entity_id1)
        self.assertIsNotNone(read_entity)
        self.assertEqual(test_entity1.id, read_entity.id)
        self.assertEqual(test_entity1.url, read_entity.url)
        #self.assertEqual(test_entity3.last_check.timestamp(), read_entity.last_check.timestamp())

        # Unable to read an entity by wrong id
        read_entity = self._datastore.get_by_id(DummyEntity, 123123812381)
        self.assertIsNone(read_entity)

        # Get entity 2 by url
        read_entities = self._datastore.get_by_property(DummyEntity, "url", "=", test_entity2.url)
        self.assertEqual(1, len(read_entities))
        read_entity = read_entities[0]
        self.assertIsNotNone(read_entity)
        self.assertEqual(test_entity2.id, read_entity.id)
        self.assertEqual(test_entity2.url, read_entity.url)
        #self.assertEqual(test_entity2.last_check.timestamp(), read_entity.last_check.timestamp())

        # Unable to read an entity by wrong url
        read_entities = self._datastore.get_by_property(DummyEntity, "url", "=", "RANDOM_URL_NOT_EXISTING")
        self.assertEqual(0, len(read_entities))


        # ---- Tests for updating entities from the datastore ----
        test_entity2_new = self._create_dummy_entity()
        test_entity2.url = test_entity2_new.url
        test_entity2.last_check = test_entity2_new.last_check
        entity_id2_new = self._datastore.put(test_entity2)
        self.assertEqual(entity_id2, entity_id2_new) # Check is the same id
        read_entity = self._datastore.get_by_id(DummyEntity, entity_id2)
        self.assertIsNotNone(read_entity)
        self.assertEqual(test_entity2.id, read_entity.id)
        self.assertEqual(test_entity2.url, read_entity.url)
        #self.assertEqual(test_entity4.last_check.timestamp(), read_entity.last_check.timestamp())
        

        # ---- Tests for deleting entities from the datastore ----
        # Delete 1 entity
        self._datastore.delete_by_id(DummyEntity, entity_id1)
        # It should still work, despite the entity is not present anymore
        self._datastore.delete_by_id(DummyEntity, entity_id1)
        # To be sure, check database for entity 1
        read_entity = self._datastore.get_by_id(DummyEntity, entity_id1)
        self.assertIsNone(read_entity)
        read_entities = self._datastore.get_all(DummyEntity)
        self.assertEqual(2, len(read_entities))

        # Delete all the entities
        self._datastore.delete_all(DummyEntity)
        read_entities = self._datastore.get_all(DummyEntity)
        self.assertEqual(0, len(read_entities))

    def _create_dummy_entity(self) -> DummyEntity:
        """Created an entity with some test data
        """
        test_item = DummyEntity()
        timenow = datetime.datetime.now()
        test_item.url = "testing_url_{}".format(timenow)
        test_item.last_check = timenow
        return test_item



