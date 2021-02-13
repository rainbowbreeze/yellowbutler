"""Implements storage service using Google Cloud Firestore in Datastore mode

Docs:
- https://cloud.google.com/appengine/docs/standard/python3/using-cloud-datastore
- https://cloud.google.com/datastore/docs/concepts/overview - top-level concepts to know
- https://cloud.google.com/datastore/docs/concepts - with main datastore concepts
- https://googleapis.dev/python/datastore/latest/client.html - API reference for the google python client
- 

Misc
- Free quota: https://cloud.google.com/datastore/pricing

Authentication improvements
- https://www.bernardorodrigues.org/post/bypass-app-engine-auth-local
- https://github.com/googleapis/google-cloud-python/issues/9097

Codice da vedere
- https://github.com/cirbuk/datastore-orm/blob/master/datastore_orm/model.py
"""

from typing import List, Optional, Type, TypeVar, Union
import datetime

from google.cloud import datastore

from yellowbot.loggingservice import LoggingService
from yellowbot.storage.basestorageservice import BaseStorageService, BaseEntity

# See here for explanation: https://www.python.org/dev/peps/pep-0484/#the-type-of-class-objects
BE = TypeVar('BE', bound=BaseEntity)

class DatastoreStorageService(BaseStorageService):
    """This class implements the storage interface using Google Cloud Firestore in Datastore mode

    Datastore requires a Kind for the entities to save into the db.
     https://cloud.google.com/datastore/docs/concepts/entities#kinds_and_identifiers
     The name of the specific entity class is used
    """

    def __init__(self) -> None:
        """Initialize the class
        """
        super().__init__()
        self._client = datastore.Client()  # Client will contain the class
        self._logger = LoggingService.get_logger(__name__)


    def put(self, entity: BE) -> int:
        """Save an entity in the datastore, or update an existing one

        :param entity: the entity to save
        :type entity: a class that inherits BaseEntity

        :returns: the id of the entity
        :rtype: int

        :raises: ValueError if entity is not a subclass of BaseEntity
        """
        
        # Just to be sure the given class is a subclass of BaseEntity
        if not isinstance(entity, BaseEntity):
            raise ValueError("Param entity has to be subclass of BaseEntity")

        kind = entity.get_entity_name()
        if BaseEntity.NO_ID == entity.id:
            self._logger.debug("Saving a new item of kind {}".format(kind))
            key = self._client.key(kind)
        else:
            self._logger.debug("Updating an existing item of kind {} with id {}".format(kind, entity.id))
            key = self._client.key(kind, entity.id)

        with self._client.transaction():       
            datastore_entity = datastore.Entity(key=key)
            # Updates all the fields of the entity
            datastore_entity.update(entity.to_dict())
            self._client.put(datastore_entity)

        if BaseEntity.NO_ID == entity.id:
            entity.id = datastore_entity.key.id

        return entity.id

    def get_all(self, entity_class: Type[BE]) -> List[BE]:
        """Returns all the entities for the given type

        :param entity_class: the final Entity where to put data
        :type entity_class: a subclass of BaseEntity

        :raises: ValueError if entity_class is not a subclass of BaseEntity
        """

        # Just to be sure the given class is a subclass of BaseEntity
        if not issubclass(entity_class, BaseEntity):
            raise ValueError("Param entity_class has to be subclass of BaseEntity")

        kind = entity_class.get_entity_name()
        self._logger.info("Getting all the entities of kind {}".format(kind))
        query = self._client.query(kind=kind)
        datastore_results = list(query.fetch())

        entity_list = []
        for datastore_item in datastore_results:
            # Create a new entity to store the data
            new_entity = self._create_entity_from_datastore(entity_class,  datastore_item)
            entity_list.append(new_entity)
            # print("ID {} - {}".format(entity.id, entity))

        return entity_list

    def get_by_id(self, entity_class: Type[BE], entity_id: int) -> Optional[BE]:
        """Finds a specific entity given its id

        :param entity_class: the final Entity where to put data
        :type entity_class: a subclass of BaseEntity

        :param entity_id: the id of the entity
        :type entity_id: int

        :raises: ValueError if entity_class is not a subclass of BaseEntity
        """

        # Just to be sure the given class is a subclass of BaseEntity
        if not issubclass(entity_class, BaseEntity):
            raise ValueError("Param entity_class has to be subclass of BaseEntity")

        kind = entity_class.get_entity_name()
        self._logger.debug("Get entity of kind {} and with id = {}".format(
            kind,
            entity_id
        ))
        key = self._client.key(kind, entity_id)
        datastore_result = self._client.get(key)

        # Using a query, instead
        #query = self._client.query(kind=kind)
        #key = self._client.key(kind, entity_id)
        #query.key_filter(key, "=")        
        #results = list(query.fetch())

        new_entity = None
        if not None is datastore_result:
            new_entity = self._create_entity_from_datastore(entity_class,  datastore_result)
 
        return new_entity

    def get_by_property(
        self,
        entity_class: Type[BE],
        property_name: str,
        operator: str,
        property_value: Union[int, str, bool, float, None, datetime.date]
    ) -> List[BE]:
        """Finds a specific entity given its id

        :param entity_class: the final Entity where to put data
        :type entity_class: a subclass of BaseEntity

        :param property_name: the id of the entity
        :type property_name: str

        :param operator: what's the comparison applied between the property and the value
        :type operator: str

        :param property_value: what's the comparison applied between the property and the value
        :type property_value: int, str, bool, float, NoneType, datetime.datetime

        :returns: a list of entity matching the search criteria
        :rtype: list

        :raises: ValueError if entity_class is not a subclass of BaseEntity
        """

        # Just to be sure the given class is a subclass of BaseEntity
        if not issubclass(entity_class, BaseEntity):
            raise ValueError("Param entity_class has to be subclass of BaseEntity")

        kind = entity_class.get_entity_name()
        self._logger.debug("Searching for entity of kind {} with {} {} ##{}## (## excluded)".format(
            kind,
            property_name,
            operator,
            property_value
        ))
        query = self._client.query(kind=kind)
        query.add_filter(property_name, operator, property_value)
        datastore_results = list(query.fetch())

        entity_list = []
        for datastore_item in datastore_results:
            # Create a new entity to store the data
            new_entity = self._create_entity_from_datastore(entity_class,  datastore_item)
            entity_list.append(new_entity)

        return entity_list

    def delete_all(self, entity_class: Type[BE]) -> None:
        """Delete all the entiries of the given type

        :param entity_class: the class of the Entity to delete
        :type entity_class: a subclass of BaseEntity

        :raises: ValueError if entity_class is not a subclass of BaseEntity
        """

        # Just to be sure the given class is a subclass of BaseEntity
        if not issubclass(entity_class, BaseEntity):
            raise ValueError("Param entity_class has to be subclass of BaseEntity")

        kind = entity_class.get_entity_name()
        self._logger.info("Deleting all the entities of kind {}".format(kind))
        query = self._client.query(kind=kind)
        query.keys_only()

        datastore_keys = list(query.fetch())
        self._client.delete_multi(datastore_keys)

    def delete_by_id(self, entity_class: Type[BE], entity_id: int) -> None:
        """Delete a specific entity given its id

        :param entity_class: the final Entity where to put data
        :type entity_class: a subclass of BaseEntity

        :param entity_id: the id of the entity
        :type entity_id: int

        :raises: ValueError if entity_class is not a subclass of BaseEntity
        """

        # Just to be sure the given class is a subclass of BaseEntity
        if not issubclass(entity_class, BaseEntity):
            raise ValueError("Param entity_class has to be subclass of BaseEntity")

        kind = entity_class.get_entity_name()
        self._logger.debug("Delete entity of kind {} and with id = {}".format(
            kind,
            entity_id
        ))
        key = self._client.key(kind, entity_id)
        self._client.delete(key)

    def _create_entity_from_datastore(
        self,
        entity_class: Type[BE],
        datastore_item: datastore.entity.Entity
    ) -> BE:
        """Instantiace a new entity using data from Datastore
        """
        new_entity = entity_class()
        new_entity.from_dict(datastore_item)
        new_entity.id = datastore_item.key.id
        return new_entity
