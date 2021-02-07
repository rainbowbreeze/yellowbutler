"""Generic class for implementing a storage service

Subclasses have to implement the most important method, using the storage
they prefer
"""

from typing import Optional

from yellowbot.storage.baseentity import BaseEntity

class BaseStorageService():
    """Define a generic interface for a storage service
    """
    def __init__(self) -> None:
        """Initialize the class
        """
        pass

    def put(self, entity: BaseEntity) -> int:
        """Save an entity in the datastore, or update an existing one

        :param entity: the entity to save
        :type entity: a class that inherits BaseEntity

        :returns: the id of the entity
        :rtype: int

        :raises: ValueError if entity is not a subclass of BaseEntity
        """
        
        raise ValueError("put method wasn't implemented for {}".format(self.__class__.__name__))

    def get_all(self, entity_class) -> list:
        """Returns all the entities for the given type

        :param entity_class: the final Entity where to put data
        :type entity_class: a subclass of BaseEntity

        :raises: ValueError if entity_class is not a subclass of BaseEntity
        """

        raise ValueError("get_all method wasn't implemented for {}".format(self.__class__.__name__))

    def get_by_id(self, entity_class, entity_id: int) -> Optional[BaseEntity]:
        """Finds a specific entity given its id

        :param entity_class: the final Entity where to put data
        :type entity_class: a subclass of BaseEntity

        :param entity_id: the id of the entity
        :type entity_id: int

        :raises: ValueError if entity_class is not a subclass of BaseEntity
        """

        raise ValueError("get_by_id method wasn't implemented for {}".format(self.__class__.__name__))

    def get_by_property(self, entity_class, property_name: str, operator: str, property_value: object) -> list:
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

        raise ValueError("get_by_property method wasn't implemented for {}".format(self.__class__.__name__))

    def delete_all(self, entity_class) -> None:
        """Delete all the entiries of the given type

        :param entity_class: the class of the Entity to delete
        :type entity_class: a subclass of BaseEntity

        :raises: ValueError if entity_class is not a subclass of BaseEntity
        """

        raise ValueError("delete_all method wasn't implemented for {}".format(self.__class__.__name__))

    def delete_by_id(self, entity_class, entity_id: int) -> None:
        """Delete a specific entity given its id

        :param entity_class: the final Entity where to put data
        :type entity_class: a subclass of BaseEntity

        :param entity_id: the id of the entity
        :type entity_id: int

        :raises: ValueError if entity_class is not a subclass of BaseEntity
        """

        raise ValueError("delete_by_id method wasn't implemented for {}".format(self.__class__.__name__))
