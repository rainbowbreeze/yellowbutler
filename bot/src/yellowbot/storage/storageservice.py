"""Generic class for implementing a storage service

Subclasses have to implement the most important method, using the storage
they prefer
"""

class StorageService():
    """Define a generic interface for a storage service
    """
    def __init__(self):
        pass

    def save(self, entity: dict):
        """Save a generic entity in the storage service

        :param entity: the entity to save, in a generic format inside of a dict
        :type entity: dict
        """
        pass

    def query(self):
        pass
        
