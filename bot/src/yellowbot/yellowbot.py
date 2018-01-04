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
from yellowbot.gears.weathergear import WeatherGear
from yellowbot.globalbag import GlobalBag
from yellowbot.loggingservice import LoggingService
from yellowbot.nluengine import NluEngine
from yellowbot.schedulerservice import SchedulerService
from yellowbot.surfaces.surfacemessage import SurfaceMessage
from yellowbot.surfaces.telegramnotifyadminsurface import TelegramNotifyAdminSurface
from yellowbot.surfaces.telegramsurface import TelegramSurface


class YellowBot:
    """
    The Yellow bot core class. Orchestrate the connections between the external world and the gears
    """

    def __init__(self,
                 nlu_engine=None,
                 scheduler=None,
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

        # Create the logger and initialise it
        self._logger = LoggingService.get_logger(__name__)
        self._logger.info("YellowBot is starting")

        # Load the config file
        self._load_config_file(config_file)

        # Creates the datastore service
        db_filename = os.path.join(os.path.dirname(__file__), GlobalBag.DATABASE_FILE)
        self._datastore = DatastoreService(db_filename)

        # Registers the interaction surface
        self._surfaces = {}
        self._register_interaction_surfaces(test_mode)

        # Registers gears
        self._gears = []
        self._register_gears()

        # Assigns the NLU engine
        self._nlu_engine = nlu_engine if nlu_engine is not None else NluEngine()

        # Assigns the scheduler service
        self._scheduler = scheduler if scheduler is not None else SchedulerService(GlobalBag.SCHEDULER_FILE)

    def _load_config_file(self, config_file):
        """
        Load config key/value pairs from a file
        :param config_file: name of the file. Can be full path or, otherwise,
        same folder of this class is considered
        :type config_file: str

        :return:
        """
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

    def _register_interaction_surfaces(self, test_mode):
        """
        Registers all the notification surfaces

        :param test_mode: class instance created for test purposes, some
        features are disabled
        :type test_mode: bool

        """
        running_on_pythonanywhere = self.get_config("running_on_pythonanywhere_free", throw_error=False)

        # NotifyAdmin surface
        self._surfaces[GlobalBag.SURFACE_NOTIFY_ADMIN] = TelegramNotifyAdminSurface(
            GlobalBag.SURFACE_NOTIFY_ADMIN,
            self.get_config("telegram_notifyadmin_authorization_token"),
            self.get_config("telegram_notifyadmin_chat_id"),
            running_on_pythonanywhere=running_on_pythonanywhere,
            test_mode=test_mode
        )

        # Telegram bot Lurch
        self._surfaces[GlobalBag.SURFACE_TELEGRAM_BOT_LURCH] = TelegramSurface(
            GlobalBag.SURFACE_TELEGRAM_BOT_LURCH,
            self.get_config("telegram_lurch_authorization_token"),
            self.get_config("base_vps_address") + self.get_config("telegram_lurch_webhook_url_relative"),
            running_on_pythonanywhere=running_on_pythonanywhere,
            test_mode=test_mode
        )


    def _register_gears(self):
        """
        Registers all the gears in the bot
        """
        self._gears.append(MusicGear())
        self._gears.append(EchoMessageGear())
        self._gears.append(WeatherGear())
        self._gears.append(EasyNidoGear(
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

    def add_interaction_surface(self, key, interaction_surface):
        """
        Add a new interaction surface

        :param key: the key to assign to the interaction surface
        :type key: str

        :param interaction_surface: the surface to add
        :type interaction_surface: BaseInteractionSurface
        """
        self._surfaces[key] = interaction_surface

    def send_message(self, message):
        """
        Sends a message to one of the interaction surfaces.
        Use this method when YellowBot acts as a chatbot

        :param message: the message received that needs to be handled
        :type message: SurfaceMessage
        """
        # Finds the surface for sending the result message
        surface = self._surfaces[message.surface_id] if message.surface_id in self._surfaces else None
        if surface is not None:
            # Creates a new message and dispatch it
            return surface.send_message(message)
        else:
            raise ValueError("Cannot find a surface to process message for {}".format(message.surface_id))

    def notify_admin(self, text):
        """
        Sends a notification to the admin. Use in very few cases and, under
         the hood, uses a dedicated interaction surface targeting a special
         channel used by admin

        :param text: the message to send
        :type text: str
        :return:
        """
        # Finds the surface for sending the result message
        admin_surface = self._surfaces[GlobalBag.SURFACE_NOTIFY_ADMIN]\
            if GlobalBag.SURFACE_NOTIFY_ADMIN in self._surfaces\
            else None
        if admin_surface is not None:
            self._logger.info("Notify admin about %s", text)
            # Creates a new message and dispatch it
            message = admin_surface.forge_notification(text)
            return admin_surface.send_message(message)
        else:
            self._logger.info("Cannot notify admin about %s", text)
            raise ValueError("Cannot find an admin surface to process message for {}".format(GlobalBag.SURFACE_NOTIFY_ADMIN))

    def receive_message(self, message):
        """
        Process a message that hits one of the interaction surface.
        Use this method when YellowBot acts as a chatbot

        :param message: the message received that needs to be handled
        :type message: SurfaceMessage

        :return: TBD
        """
        if not message:
            self._logger.info("A message was received, but has no data inside")
            return

        # Finds how to process the message
        intent, params = self._nlu_engine.infer_intent_and_args(message.text)
        # If an intent is matched, process the intent and return the result
        #  of the operation
        self._logger.info("The message received triggered the intent %s", intent)

        if intent:
            response_text = self.process_intent(intent, params)
        else:
            # Fallback call: Does a simple echo of the message
            response_text = "I don't know how to process what you said: '{}'".format(message.text)

        # If there is nothing as response text, well... Job is done!
        if not response_text:
            return

        # Finds the surface for sending the result message
        surface = self._surfaces[message.surface_id] if message.surface_id in self._surfaces else None
        if surface is not None:
            # Creates a new message and dispatch it
            return surface.send_message(SurfaceMessage(
                message.surface_id,
                message.channel_id,
                response_text
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
        self._logger.info("Finding a gear to process intent %s", intent)
        gear = None
        for working_gear in self._gears:
            if working_gear.can_process_intent(intent):
                gear = working_gear
                break

        # And process it, if a gear has been found
        if gear is not None:
            return gear.process_intent(intent, params)
        else:
            self._logger.info("No gear found to process intent %s", intent)
            return "No gear to process your intent"

    def tick_scheduler(self):
        """
        Check for tasks to run for the scheduler service and, in case,
         executes them.

        Right now, only the hour is taken into account
        :return:
        """

        # Extracts the current time, only the hour part
        check_time = self._scheduler.get_current_hour()
        self._logger.info("Processing scheduler for time %s", check_time)

        # Checks for tasks scheduled for the current hour
        tasks = self._scheduler.find_tasks_for_time(check_time)

        if 0 == len(tasks):
            self._logger.info("No scheduled tasks found to process at the given time")
        else:
            # Executes them
            for task in tasks:
                self._logger.info("Executing scheduler task %s", task.name)
                result = self.process_intent(task.intent, task.params)
                if result is not None and task.surface is not None:
                    task.surface.text = result
                    self.send_message(task.surface)
