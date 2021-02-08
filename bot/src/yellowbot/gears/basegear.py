"""Base gear, all the others have to inherit from this one

A gear defines a way to solve one or more intents, and can be seen as a
 "feature" of the main app

Adding new gears adds more features to the main app.
"""
from typing import List, Optional, Union

class BaseGear:
    """Defines basic attributes and methods of all gears
    """

    def __init__(
        self,
        gear_name: str,
        gear_intents: List[str]
    ) -> None:
        """Constructor

        :param gear_name: name of the gear, useful for logging
        :type gear_name: str

        :param gear_intents: the intent processes
        :type gear_intents: str[]
        """

        self._gear_name = gear_name
        self._gear_intents = gear_intents

    def name(self) -> str:
        """Name of the gear

        :returns: the name of the gear
        :rtype: str
        """

        return self._gear_name

    def can_process_intent(self, intent: str) -> bool:
        """Check if the gear can process the intent

        :param intent: the intent to process
        :type intent: str

        :returns: True is this gear is able to process the intent
        :rtype: bool
        """

        # Do a ignore case comparison, maybe there is a more pythonic way to accomplish that
        for accepted_intent in self._gear_intents:
            if accepted_intent.lower() == intent.lower():
                return True
        return False

    def process_intent(
        self,
        intent: str,
        params: List[str]
    ) -> Union[Optional[str], List[str]]:
        """Process the intent. Need to be implemented in every subclass

        :param intent: the specific intent to process
        :type intent: str

        :param params: additional parameters for the intent
        :type params: dict

        :returns: a message with the result of the processing
        :rtype: str
        """

        # Union[str, List[str]] - https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html#functions
        raise ValueError("Intent processing for gear {} not implemented".format(self._gear_name))
