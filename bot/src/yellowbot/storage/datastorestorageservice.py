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

from google.cloud import datastore

from yellowbot.storage.basestorageservice import BaseStorageService, BaseEntity

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

    def put(self, entity: BaseEntity) -> int:
        """Save an entity in the datastore

        :param entity: the entity to save
        :type entity: a class that inherits BaseEntity

        :returns: the id of the entity
        :rtype: int
        """
        
        kind: str = entity.get_entity_name()
        print("kind = {}".format(kind))
        if BaseEntity.NO_ID == entity.id:
            key = self._client.key(kind)
        else:
            key = self._client.key(kind, entity.id)

        with self._client.transaction():       
            datastore_entity = datastore.Entity(key=key)
            # Updates all the fields of the entity
            datastore_entity.update(entity.to_dict())
            self._client.put(datastore_entity)

        if BaseEntity.NO_ID == entity.id:
            entity.id = datastore_entity.key.id

        return entity.id

    def query_all(self, kind:str, entity_class) -> dict:
        """Returns all the entities for the given type

        :param kind: the name of the class that will store the entities retrived
        :type kind: str

        :param entity_class:
        :type entity_class: a subclass of BaseEntity
        """

        if not issubclass(entity_class, BaseEntity):
            raise ValueError("Param entity_class has to be subclass of BaseEntity")

        query = self._client.query(kind=kind)

        datastore_results = list(query.fetch())

        entity_list = []
        for datastore_item in datastore_results:
            # Create a new entity to store the data
            new_entity = entity_class()
            new_entity.from_dict(datastore_item)
            new_entity.id = datastore_item.key.id
            entity_list.append(new_entity)
            # print("ID {} - {}".format(entity.id, entity))

        return entity_list


    def delete_all(self, kind:str) -> None:
        """Delete all the entiries of the given type

        :param kind: the name of the class that will store the entities retrived
        :type kind: str

        """
        query = self._client.query(kind=kind)
        query.keys_only()

        datastore_keys = list(query.fetch())
        self._client.delete_multi(datastore_keys)







