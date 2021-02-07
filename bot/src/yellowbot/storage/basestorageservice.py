"""Generic class for implementing a storage service

Subclasses have to implement the most important method, using the storage
they prefer
"""

from yellowbot.storage.baseentity import BaseEntity

class BaseStorageService():
    """Define a generic interface for a storage service
    """
    def __init__(self) -> None:
        pass

    def put(self, entity: BaseEntity) -> int:
        """Save a generic entity in the storage service

        :param entity: the entity to save, in a generic format inside of a dict
        :type entity: BaseEntity

        :returns: the id of the entity. A new if a new entity has been created
        :rtype: int
        """
        raise ValueError("Save method wasn't implemented for {}".format(self.__class__.__name__))

    def query(self):
        raise ValueError("Query method wasn't implemented for {}".format(self.__class__.__name__))
        
