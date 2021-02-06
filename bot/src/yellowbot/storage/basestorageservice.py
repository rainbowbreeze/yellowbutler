"""Generic class for implementing a storage service

Subclasses have to implement the most important method, using the storage
they prefer
"""

class BaseStorageService():
    """Define a generic interface for a storage service
    """
    def __init__(self):
        pass

    def save(self, entity: dict):
        """Save a generic entity in the storage service

        :param entity: the entity to save, in a generic format inside of a dict
        :type entity: dict
        """
        raise ValueError("Save method wasn't implemented for {}".format(self.__class__.__name__))

    def query(self):
        raise ValueError("Query method wasn't implemented for {}".format(self.__class__.__name__))
        
