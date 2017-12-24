"""
Main class
"""

from yellowbot.gears.musicgear import MusicGear
from yellowbot.gears.kindergartengear import KindergartenGear

class YellowBot:
    """
    Entry point for the bot
    """

    def __init__(self):
        self.keys = []
        self._gears = []
        self._register_gears()

    def _register_gears(self):
        """Registers all the gears in the bot"""
        self._gears.append(MusicGear())
        self._gears.append(KindergartenGear())

    def process_intent(self, intent, params):
        """Process an intent"""

        # Check if any of the registered gears is able to process the intent
        gear = None
        for working_gear in self._gears:
            if working_gear.can_process_intent(intent):
                gear = working_gear
                break
        if gear is not None:
            return gear.process_intent(intent, params)
        else:
            return "I don't know how to process your request"


    def echo_message(self, message):
        return "You said {}".format(message)

    def is_security_code_valid(self, security_code):
        try:
            self.keys.index(security_code)
            return True
        except ValueError:
            return False

    def unauthorize_answer(self, key):
        print("Attempt to access with a wrong key {}".format(key))
        return 404
