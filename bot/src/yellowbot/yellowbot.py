"""
Main class
"""
import json
import os

from yellowbot.gears.echomessagegear import EchoMessageGear
from yellowbot.gears.musicgear import MusicGear
from yellowbot.gears.kindergartengear import KindergartenGear
from yellowbot.nluengine import NluEngine


class YellowBot:
    """
    The Yellow bot core class. Orchestrate the connections between the external world and the gears
    """
    DEFAULT_CONFIG_FILE = "yellowbotconfig.json"

    def __init__(self,
                 nlu_engine = NluEngine(),
                 config_file = DEFAULT_CONFIG_FILE
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
        self._config = {}
        if not os.path.isfile(config_file):
            # Folder where this file is, can work also without the abspath,
            #  but better for debug so full path is traced in the error
            base_folder = os.path.abspath(os.path.dirname(__file__))
            full_config_path = os.path.join(base_folder, config_file)  # combine with the config file name
        else:
            full_config_path = config_file
        # Now if has the file and full path with configurations
        if os.path.isfile(full_config_path):
            with open(full_config_path, 'r') as f:
                self._config = json.load(f)
        else:
            raise ValueError("Cannot find configuration file {}".format(full_config_path))
        # Checks if the config files has real values
        if len(self._config.keys()) == 0:
            raise ValueError("Empty configuration file {}".format(full_config_path))

    def _register_gears(self):
        """
        Registers all the gears in the bot
        """
        self._gears.append(MusicGear())
        self._gears.append(KindergartenGear())
        self._gears.append(EchoMessageGear())

    def get_config(self, key_to_read, throw_error=True):
        """
        Read a value from the configuration, throwing an error if it doesn't exist
        :param key_to_read: the key to read
        :param throw_error: if False, doesn't throw an error, but return None instead
        :return:
        """
        try:
            return self._config[key_to_read]
        except KeyError as e:
            if throw_error:
                raise ValueError(
                    "Non existing {} value in the config, please add it".format(key_to_read))
            else:
                return None

    def is_client_authorized(self, key):
        """
        Checks if the key is among the ones authorized to use the bot
        :param key: the key to check for authorization. Authorized keys are
               generally listed in the config file
        :return: True if the key is authorized, otherwise False
        """
        if not key:
            return False

        for auth_key in self.get_config("authorized_keys"):
            if auth_key == key:
                return True
        return False

    def change_authorized_keys(self, new_keys):
        """
        Substitutes old authorization keys with new ones. Useful for testing
        purposes
        :param new_keys: new keys to use
        :return:
        """
        self._config["authorized_keys"] = new_keys

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

        :param intent: the intent to execute
        :param params: a json object with all the intent's required params
        :return: a message with the result of the processing
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
            return "No gear to process your intent"

