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

from yellowbot.storage.basestorageservice import BaseStorageService
from yellowbot.storage.baseentity import BaseEntity

class DatastoreStorageService(BaseStorageService):
    """This class implements the storage interface using Google Cloud Firestore in Datastore mode
    """

    def __init__(self):
        """Initialize the class
        """
        super().__init__()
        self._client = datastore.Client()  # Client will contain the class 

    def put(self, entity):
        """Save an entity in the datastore

        :param entity: the entity to save
        :type entity: a class that inherits BaseEntity

        :returns: the id of the entity
        :rtype: int
        """
        
        # Datastore requires a Type for the entities to save into the db.
        # The name of the specific entity class is used

        if entity.id:
            key = self._client.key(entity.entity_name, entity.id)
        else:
            key = self._client.key(entity.entity_name)

        with self._client.transaction():       
            datastore_entity = datastore.Entity(key=key)
            # Updates all the fields of the entity
            datastore_entity.update(entity.to_dict())
            self._client.put(datastore_entity)

        if not entity.id:
            entity.id = datastore_entity.key.id

        return entity.id
        

