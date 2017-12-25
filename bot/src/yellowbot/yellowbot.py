"""
Main class
"""
import json
import os

from yellowbot.gears.musicgear import MusicGear
from yellowbot.gears.kindergartengear import KindergartenGear
from yellowbot.nluengine import NluEngine


class YellowBot:
    """
    The Yellow bot core class. Orchestrate the connections between the external world and the gears
    """

    def __init__(self,
                 nlu_engine = NluEngine(),
                 config_file = "yellowbotconfig.json"
                 ):
        """
        Init the bot

        :param nlu_engine: engine to use to extract intent and arguments
        :param config_file: config file with several values. By default, the
                            file yellowbotconfig.json in the same folder of
                            this file is used, but feel free to point to any
                            other file. If only the file name is used, the
                            assumption it is in the same folder of this file
        """

        # Register gears
        self._gears = []
        self._register_gears()

        # Assign the NLU engine
        self.nlu_engine = nlu_engine

        # Load the config file
        self._load_config_file(config_file)



    def _load_config_file(self, config_file):
        # Load config file
        self.config = None
        if not os.path.isfile(config_file):
            base_folder = os.path.dirname(__file__)  # Path where this file is
            full_config_path = os.path.join(base_folder, config_file)  # combine with the config file name
        else:
            full_config_path = config_file
        if os.path.isfile(full_config_path):
            with open(full_config_path, 'r') as f:
                self.config = json.load(f)
        if self.config is None:
            raise ValueError("Cannot find configuration file {}".format(full_config_path))

    def _register_gears(self):
        """
        Registers all the gears in the bot
        """
        self._gears.append(MusicGear())
        self._gears.append(KindergartenGear())

    def is_authorized(self, key):
        """
        Checks if the key is among the ones authorized to use the bot
        :param key:
        :return: True if the key is authorized, otherwise False
        """
        for auth_key in self.config.authorized_keys:
            if auth_key == key:
                return True
        return False

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

    def is_security_code_valid(self, security_code):
        try:
            self.keys.index(security_code)
            return True
        except ValueError:
            return False

    def unauthorize_answer(self, key):
        print("Attempt to access with a wrong key {}".format(key))
        return 404
