"""
Base gear, all the others have to inherit from this one
"""


class BaseGear:
    """
    Defines basic attributes and methods of all gears
    """
    def __init__(self, gear_name, gear_intents):
        self._gear_name = gear_name
        self._gear_intents = gear_intents

    def can_process_intent(self, intent):
        """Return True is the gear process the intent, otherwise False"""

        # Do a ignore case comparison, maybe there is a more pythonic way to accomplish that
        for accepted_intent in self._gear_intents:
            if accepted_intent.lower() == intent.lower():
                return True
        return False

    def process_intent(self, intent, params):
        """Process the intent. Need to be implemented in every subclass"""
        raise ValueError("Intent processing login for gear {} not implemented".format(self._gear_name))


