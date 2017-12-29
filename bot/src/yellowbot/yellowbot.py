"""
Main class
"""
import json
import os


from json_minify import json_minify

from yellowbot.datastoreservice import DatastoreService
from yellowbot.gears.easynidogear import EasyNidoGear
from yellowbot.gears.echomessagegear import EchoMessageGear
from yellowbot.gears.musicgear import MusicGear
from yellowbot.globalbag import GlobalBag
from yellowbot.nluengine import NluEngine
from yellowbot.surfaces.surfacemessage import SurfaceMessage
from yellowbot.surfaces.telegramsurface import TelegramSurface


class YellowBot:
    """
    The Yellow bot core class. Orchestrate the connections between the external world and the gears
    """

    def __init__(self,
                 nlu_engine=None,
                 config_file=GlobalBag.CONFIG_FILE,
                 test_mode=False
                 ):
        """
        Init the bot

        :param nlu_engine: engine to use to extract intent and arguments
        :type nlu_engine: NluEngine

        :param config_file: config file with several values. By default, the
        file yellowbot_config.json in the same folder of this file is used,
        but feel free to point to any other file. If only the file name is
        used, the assumption it is in the same folder of this file
        :type config_file: str

        :param test_mode: class instance created for test purposes, some
        features are disabled
        :type test_mode: bool
        """

        # Load the config file
        self._load_config_file(config_file)

        # Creates the datastore service
        db_filename = os.path.join(os.path.dirname(__file__), GlobalBag.DATABASE_FILE)
        self._datastore = DatastoreService(db_filename)

        # Register gears
        self._gears = []
        self._register_gears()

        # Assign the NLU engine
        if nlu_engine is None:
            self.nlu_engine = NluEngine()
        else:
            self.nlu_engine = nlu_engine

        # Registers the interaction surface
        running_on_pythonanywhere = self.get_config("running_on_pythonanywhere", throw_error=False)
        self._surfaces = []
        # Telegram bot Lurch
        self._surfaces.append(TelegramSurface(
            GlobalBag.SURFACE_TELEGRAM_BOT_LURCH,
            self.get_config("telegram_lurch_authorization_token"),
            self.get_config("base_vps_address") + self.get_config("telegram_lurch_webhook_url_relative"),
            running_on_pythonanywhere=running_on_pythonanywhere,
            test_mode=test_mode
        ))

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
                json_with_comment = open(full_config_path).read()
                self._config = json.loads(json_minify(json_with_comment))
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
        self._gears.append(EchoMessageGear())
        self._gears.append(EasyNidoGear(
            self._datastore,
            self.get_config("easynido_username"),
            self.get_config("easynido_password"),
            self.get_config("easynido_idbambino")
        ))

    def get_config(self, key_to_read, throw_error=True):
        """
        Read a value from the configuration, throwing an error if it doesn't exist
        :param key_to_read: the key to read
        :type key_to_read: str

        :param throw_error: if False, doesn't throw an error, but return None instead
        :type throw_error: bool

        :return: the object associated wit the config key
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
        :type key: str

        :return: True if the key is authorized, otherwise False
        :rtype: bool
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
        :type new_keys: str
        """
        self._config["authorized_keys"] = new_keys

    def add_interaction_surface(self, interaction_surface):
        """
        Add a new interaction surface

        :param interaction_surface: the surface to add
        :type interaction_surface: BaseInteractionSurface

        :return: True if the interface has been added, otherwise false
        :rtype: bool
        """
        self._surfaces.append(interaction_surface)
        return True

    def receive_message(self, message):
        """
        Process a message that hits one of the interaction surface.
        Use this method when YellowBot acts as a chatbot

        :param message: the message received that needs to be handled
        :type message: SurfaceMessage

        :return: TBD
        """
        if not message:
            return

        # First, find how to process the message
        intent, params = self.nlu_engine.infer_intent_and_args(message.text)
        # If an intent is matched, process the intent and return the result
        #  of the operation

        # Finds the surface for sending the message
        surface = None
        for working_surface in self._surfaces:
            if working_surface.can_handle_surface(message.surface_id):
                surface = working_surface
                break

        if intent:
            text = self.process_intent(intent, params)
        else:
            # Fallback call: Does a simple echo of the message
            text = "I don't know how to process what you said: '{}'".format(message.text)

        if surface is not None:
            # Creates a new message and dispatch it
            return surface.send_message(SurfaceMessage(
                message.surface_id,
                message.channel_id,
                text
            ))
        else:
            raise ValueError("Cannot find a surface to process message for {}".format(message.surface_id))

    def process_intent(self, intent, params):
        """
        Process an intent. Use this method when YellowBot acts behind a REST API or
        something similar

        :param intent: the intent to execute
        :type intent: str

        :param params: a json object with all the intent's required params
        :type params: dict

        :return: a message with the result of the processing
        :rtype: str
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

