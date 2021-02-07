"""Base class for all the entities that need to be processed by the storage service
"""

class BaseEntity():
    """The class represents a basic data entity to save into the db

    An entity has at least two fields:
    - id: an integer with the key of the entity
       It's automatically managed by the storage service
    - entity_name: a string that uniquely identifies the entity type.
       Generally the class name is used, so the same entities have the same name
    """

    def __init__(self):
        self.id = None
        self.entity_name = self.__class__.__name__
        # Change in inherited initialization method, if needed

    def to_dict(self):
        """Transform the entity data in a dictionaty.

        It has to be implemented in subclasses

        :returns: a dict containing all the important values of the entity
        :rtype: dict
        """

        raise ValueError("Method to_dict in {} has not been implemented".format(self.__class__.__name__))