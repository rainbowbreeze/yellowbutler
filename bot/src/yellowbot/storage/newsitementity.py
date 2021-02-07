"""
https://docs.python.org/3/tutorial/datastructures.html#dictionaries
"""

from datetime import date
from yellowbot.storage.baseentity import BaseEntity

class NewsItemEntity(BaseEntity):
    """Entity to store information about a news item
    """
    url: str
    last_check: date
    param1: str

    def __init__(self) -> None:
        """
        """
        super().__init__()  # Sets fundamental entity properties
        self.url: None
        self.last_check: None
        self.param1: None

    @staticmethod
    def get_entity_name() -> str:
        """Returns the name of the class only, not the package + name
        """
        return __class__.__name__

    def to_dict(self) -> dict:
        """Transform the entity values in a dict
        
        :returns: a dict containing the entity values
        :rtype: dict
        """

        fields = {}
        if hasattr(self, "url"):
            fields["url"] = self.url
        if hasattr(self, "last_check"):
            fields["last_check"] = self.last_check
        if hasattr(self, "param1"):
            fields["param1"] = self.param1
        return fields

    def from_dict(self, source_dict: dict):
        """Create the entity data from a dict
        """
        if hasattr(source_dict, "url"):
            self.url = source_dict["url"]
        if hasattr(source_dict, "last_check"):
            self.last_check = source_dict["last_check"]
        if hasattr(source_dict, "param1"):
            self.param1 = source_dict["param1"]

        return self
        

