"""YellowBot main class, everything starts from here
"""

from re import M
from sys import exc_info
from typing import Any, Dict, List, Optional
from yellowbot.configservice import ConfigService
from yellowbot.gears.basegear import BaseGear
from yellowbot.gears.easynidogear import EasyNidoGear
from yellowbot.gears.echomessagegear import EchoMessageGear
from yellowbot.gears.gearexecutionresult import GearExecutionResult
from yellowbot.gears.musicgear import MusicGear
from yellowbot.gears.notifyadmingear import NotifyAdminGear
from yellowbot.gears.sendmessagegear import SendMessageGear
from yellowbot.gears.weathergear import WeatherGear
from yellowbot.gears.commitstripgear import CommitStripGear
from yellowbot.gears.newsreportergear import NewsReportGear
from yellowbot.globalbag import GlobalBag
from yellowbot.loggingservice import LoggingService
from yellowbot.nluengine import NluEngine
from yellowbot.schedulerservice import SchedulerService
from yellowbot.storage.datastorestorageservice import DatastoreStorageService
from yellowbot.storage.basestorageservice import BaseStorageService
from yellowbot.surfaces.surfacemessage import SurfaceMessage


class YellowBot:
    """The Yellow bot core class. Orchestrate the connections between the external world and the gears
    """

    def __init__(
        self,
        nlu_engine: NluEngine = None,
        scheduler: SchedulerService = None,
        config_file:str = GlobalBag.CONFIG_FILE,
        test_mode: bool = False
    ) -> None:
        """Init the bot

        :param nlu_engine: engine to use to extract intent and arguments
        :type nlu_engine: NluEngine

        :param scheduler: the scheduler service
        :type scheduler: SchedulerService

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
        self._config_service = ConfigService(config_file)

        # Creates the datastore service
        # db_filename = os.path.join(os.path.dirname(__file__), GlobalBag.DATABASE_FILE)
        # self._datastore = DatastoreService(db_filename)

        # Registers gears
        self._gears: List[BaseGear] = []
        self._register_gears(test_mode)

        # Assigns the NLU engine
        self._nlu_engine = nlu_engine if nlu_engine is not None else NluEngine()

        # Assigns the scheduler service
        self._scheduler = scheduler if scheduler is not None else SchedulerService(GlobalBag.SCHEDULER_FILE)

    def _register_gears(self, test_mode: bool) -> None:
        """Registers all the gears in the bot

        :param test_mode: class instance created for test purposes, some
        features are disabled
        :type test_mode: bool
        """

        self._gears.append(MusicGear(
            self._config_service.get_config("tracemusic_destination_url"),
            test_mode
        ))
        self._gears.append(EchoMessageGear())
        self._gears.append(WeatherGear(
            self._config_service.get_config("darksky_api")
        ))
        #self._gears.append(EasyNidoGear(
        #    self._config_service.get_config("easynido_username"),
        #    self._config_service.get_config("easynido_password"),
        #    self._config_service.get_config("easynido_bambini")
        #))

        # Admin notification gear
        self._gears.append(NotifyAdminGear(
            self._config_service,
            test_mode
        ))

        # Send message gear
        self._gears.append(SendMessageGear(
            self._config_service,
            test_mode
        ))

        # CommitStrip gear
        self._gears.append(CommitStripGear())

        # CheckForNews gear
        storage_service = DatastoreStorageService() if not test_mode else BaseStorageService()
        self._gears.append(NewsReportGear(
            self._config_service.get_config("youtube_api"),
            self._config_service.get_config("newssources_urls"),
            storage_service
        ))

    def get_config(
        self,
        key_to_read: str,
        throw_error:bool = True
    ) -> Any:
        """Read a value from the configuration, throwing an error if it doesn't exist
        :param key_to_read: the key to read
        :type key_to_read: str

        :param throw_error: if False, doesn't throw an error, but return None instead
        :type throw_error: bool

        :returns: the object associated wit the config key
        :rtype: obj
        """

        return self._config_service.get_config(key_to_read, throw_error)
        # TODO fix this workaround for Flask

    def is_client_authorized(self, key: str) -> bool:
        """Checks if the key is among the ones authorized to use the bot

        :param key: the key to check for authorization. Authorized keys are
        generally listed in the config file
        :type key: str

        :returns: True if the key is authorized, otherwise False
        :rtype: bool
        """

        if not key:
            return False

        for auth_key in self._config_service.get_config("authorized_keys"):
            if auth_key == key:
                return True
        return False

    def change_authorized_keys(self, new_keys: List[str]):
        """Substitutes old authorization keys with new ones. Useful for testing purposes

        :param new_keys: new keys to use
        :type new_keys: str
        """

        self._config_service.change_authorized_keys(new_keys)
        # TODO fix workaround for tests

    def notify_admin(self, message: str) -> None:
        """Sends a notification to the admin.
        
        Use in very few cases and, under the hood, it's the usual intent
         process, using a dedicated interaction surface targeting a special
         channel used by admin

        :param message: the message to send
        :type message: str
        
        :returns: None
        :rtype: None
        """

        result = self.process_intent(
            GlobalBag.NOTIFY_ADMIN_INTENT,
            {
                GlobalBag.NOTIFY_ADMIN_PARAM_MESSAGE: message
            }
        )
        if not result.went_well():
            self._logger.error("Error in notifing the admin with this message: {}".format(message))
            for message in result.get_messages():
                self._logger.error("Root cause: {}".format(message))

    def process_intent(
        self,
        intent: str,
        params: Dict[str, Any]
    ) -> GearExecutionResult:
        """Process an intent. Use this method when YellowBot acts behind a REST API or something similar.
        
        :param intent: the intent to execute
        :type intent: str

        :param params: a json object with all the intent's required params
        :type params: dict

        :returns: a message with the result of the processing
        :rtype: str
        """

        # Check if any of the registered gears is able to process the intent
        self._logger.info("Finding a gear to process intent {}".format(intent))
        gear = None
        for working_gear in self._gears:
            if working_gear.can_process_intent(intent):
                gear = working_gear
                break

        # And process it, if a gear has been found
        # The expectation is that each gear process its own errors, so
        #  no errors bubble up at this level
        if gear is not None:
            # self._logger.debug("Found gear {}".format(gear.name()))
            return gear.process_intent(intent, params)
        else:
            self._logger.info("No gear found to process intent {}".format(intent))
            return GearExecutionResult.ERROR("No gear to process your intent")

    def receive_message(self, surface_message: SurfaceMessage) -> None:
        """Process a message that hits one of the interaction surface.
        Use this method when YellowBot acts as a chatbot

        :param message: the message received that needs to be handled
        :type message: SurfaceMessage

        :returns: the interaction surface sending message operation result, TBD
        :rtype: 
        """
        
        if not surface_message:
            self._logger.info("A message was received, but has no data inside")
            return

        # Finds how to process the message
        intent, params = self._nlu_engine.infer_intent_and_args(surface_message.text)
        # If an intent is matched, process the intent and return the result
        #  of the operation
        self._logger.info("The message received triggered the intent {} ".format(intent))

        output_messages = None
        if intent:
            execution_result = self.process_intent(intent, params)
            output_messages = execution_result.get_messages()
        else:
            # Fallback call: Does a simple echo of the message arrived from the surface
            output_messages = []
            output_messages.append("I don't know how to process what you said: '{}'".format(surface_message.text))

        # Send potential messages to the calling surface        
        self._send_multiple_messages_to_a_surface(
            surface_message.surface_id,
            surface_message.channel_id,
            output_messages)

    def tick_scheduler(self):
        """Check for tasks to run for the scheduler service and, in case, executes them.

        Right now, only the hour is taken into account
        """

        check_time = self._scheduler.get_current_datetime()
        self._logger.info("Processing scheduler for time {}".format(check_time))

        tasks = self._scheduler.find_tasks_for_time(check_time)

        if 0 == len(tasks):
            self._logger.info("No scheduled tasks found to process at the given time")
        else:
            # Executes them
            for task in tasks:
                self._logger.info("Executing scheduler task {}".format(task.name))
                execution_result = self.process_intent(task.intent, task.params)

                if task.surface is not None:
                    self._logger.debug("Task executed, sending the result to the surface {} channel_id {}")
                    output_messages = None
                    # If the intent has returned something, use that text, otherwise the default
                    #  text in the configuration file
                    if execution_result.has_messages:
                        output_messages = execution_result.get_messages()
                    else:
                        if task.default_message:
                            output_messages = []
                            output_messages.append(task.default_message)
                    
                    self._send_multiple_messages_to_a_surface(
                        task.surface.surface_id,
                        task.surface.channel_id,
                        output_messages)
    
    def _send_multiple_messages_to_a_surface(
        self,
        surface_id: Optional[str],
        channel_id: Optional[str],
        messages) -> None:
        """Send multiple messages to a surface, generated by the output of a
        scheduled job or a call from a surface
        """

        # If there is nothing as response text, well... Job is done!
        if not messages or 0 == len(messages):
            return

        for output_message in messages:
            # Skip empty messages
            if not output_message:
                self._logger.info("Empty message") #TODO remove the line
                continue

            # It could happen that the main intent is process, but the following
            #  intent, that communicates back to the interaction surface, fails
            #  because of a strange reason, like a misformatted text, etc.
            # So, as last resource, the error in processed _also_ here, but the
            #  expectation is that each gear process the error by itself, so
            #  an error condition here should never happen
            try:
                # create a reply, and send it back
                self.process_intent(
                    GlobalBag.SEND_MESSAGE_INTENT,
                    {
                        GlobalBag.SEND_MESSAGE_PARAM_SURFACE_ID: surface_id,
                        GlobalBag.SEND_MESSAGE_PARAM_CHANNEL_ID: channel_id,
                        GlobalBag.SEND_MESSAGE_PARAM_TEXT: output_message
                    }
                )
            except BaseException as err:
                self._logger.exception("Unexpected error in sending the intent result message back to the surface: {}".format(err))
                # Tries to communicate back to the surface that it was an error
                self.process_intent(
                    GlobalBag.SEND_MESSAGE_INTENT,
                    {
                        GlobalBag.SEND_MESSAGE_PARAM_SURFACE_ID: surface_id,
                        GlobalBag.SEND_MESSAGE_PARAM_CHANNEL_ID: channel_id,
                        GlobalBag.SEND_MESSAGE_PARAM_TEXT: "The request was executed, but they were issues in communicating back the result. Please check server logs for more info"
                    }
                )

