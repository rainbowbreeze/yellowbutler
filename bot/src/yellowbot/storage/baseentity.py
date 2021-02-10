"""Base class for all the entities that need to be processed by the storage service
"""

# Reference for the  type hint of the same (enclosing) class
# https://stackoverflow.com/questions/33533148/how-do-i-type-hint-a-method-with-the-type-of-the-enclosing-class

from typing import Any, ClassVar, Dict

class BaseEntity():
    """The class represents a basic data entity to save into the db

    An entity has at least two fields:
    - id: an integer with the key of the entity
       It's automatically managed by the storage service
    - entity_name: a string that uniquely identifies the entity type.
       Generally the class name is used, so the same entities have the same name
    """

    NO_ID: ClassVar[int] = 0  # when the id has this value, it means it hasn't been assigned
    id: int

    def __init__(self) -> None:
        self.id = BaseEntity.NO_ID  # 0 means no id
        # Change in inherited initialization method, if needed

    @staticmethod
    def get_entity_name() -> str:
        """Returns the name of the class. Has to be overwritten by subclasses

        To keep it easy, subclasses can return __class__.__name__
         (return only the name of the class, not the whole path)
        """
        raise ValueError("Method get_entity_name has not been implemented")

    def to_dict(self) -> Dict[str, Any]:
        """Transform the entity data in a dictionaty.

        It has to be implemented in subclasses

        :returns: a dict containing all the important values of the entity
        :rtype: dict
        """

        raise ValueError("Method to_dict in {} has not been implemented".format(self.__class__.__name__))

    def from_dict(self, source_dict: dict) -> 'BaseEntity':
        """Create the entity from a dict

        It has to be implemented in subclasses
        """

        raise ValueError("Method from_dict has not been implemented")    