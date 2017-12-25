"""
Main class
"""

from yellowbot.gears.musicgear import MusicGear
from yellowbot.gears.kindergartengear import KindergartenGear
from yellowbot.nluengine import NluEngine


class YellowBot:
    """
    The Yellow bot core class. Orchestrate the connections between the external world and the gears
    """

    def __init__(self,
                 nlu_engine = NluEngine(),
                 ):
        """
        Init the bot

        :param nlu_engine: engine to use to extract intent and arguments
        """
        self.keys = []
        self._gears = []
        self._register_gears()
        self.nlu_engine = nlu_engine

    def _register_gears(self):
        """
        Registers all the gears in the bot
        """
        self._gears.append(MusicGear())
        self._gears.append(KindergartenGear())

    def infer_intent_and_params(self, chat_message):
        """
        Find intent and arguments from a chat message. Use this method when YellowBot
        acts as a chatbot

        :param chat_message:
        :return:
        """
        return self.nlu_engine.infer_intent_and_args(chat_message)
        pass

    def process_intent(self, intent, params):
        """
        Process an intent. Use this method when YellowBot acts behind a REST API or
        something similar

        :param intent:
        :param params:
        :return:
        """

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
