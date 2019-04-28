"""
A gear to send message using a interaction surface
"""

from yellowbot.gears.basegear import BaseGear
from yellowbot.globalbag import GlobalBag
from yellowbot.loggingservice import LoggingService
from yellowbot.surfaces.surfacemessage import SurfaceMessage
from yellowbot.surfaces.telegramnotifyadminsurface import TelegramNotifyAdminSurface
from yellowbot.surfaces.telegramsurface import TelegramSurface


class SendMessageGear(BaseGear):
    """
    Get the weather condition from Yahoo! Weather service
    """
    INTENTS = [GlobalBag.SEND_MESSAGE_INTENT]
    PARAM_SURFACE_ID = GlobalBag.SEND_MESSAGE_PARAM_SURFACE_ID
    PARAM_CHANNEL_ID = GlobalBag.SEND_MESSAGE_PARAM_CHANNEL_ID
    PARAM_TEXT = GlobalBag.SEND_MESSAGE_PARAM_TEXT

    def __init__(self,
                 config_service,
                 test_mode=False):
        """
        Init the class

        :param config_service: configuration service
        :type config_service: ConfigService

        :param test_mode: class instance created for test purposes, some
        features are disabled
        :type test_mode: bool
        """
        BaseGear.__init__(self, SendMessageGear.__name__, self.INTENTS)
        self._config_service = config_service
        self._logger = LoggingService.get_logger(__name__)

        # Registers the interaction surface
        self._surfaces = {}
        self._register_interaction_surfaces(test_mode)

    def process_intent(self, intent, params):
        """
        Sends a message using one of the registered surfaces

        :param intent:
        :param params:
        :return:
        """
        if SendMessageGear.PARAM_SURFACE_ID not in params:
            return "Missing {} parameter in the request".format(SendMessageGear.PARAM_SURFACE_ID)
        if SendMessageGear.PARAM_CHANNEL_ID not in params:
            return "Missing {} parameter in the request".format(SendMessageGear.PARAM_CHANNEL_ID)
        if SendMessageGear.PARAM_TEXT not in params:
            return "Missing {} parameter in the request".format(SendMessageGear.PARAM_TEXT)

        message = SurfaceMessage(
            params[SendMessageGear.PARAM_SURFACE_ID],
            params[SendMessageGear.PARAM_CHANNEL_ID],
            params[SendMessageGear.PARAM_TEXT]
        )
        self._logger.info("Sending message to surface id {}".format(message.surface_id))
        return self._send_message(message)

    def add_interaction_surface(self, key, interaction_surface):
        """
        Add a new interaction surface

        :param key: the key to assign to the interaction surface
        :type key: str

        :param interaction_surface: the surface to add
        :type interaction_surface: BaseInteractionSurface
        """
        self._surfaces[key] = interaction_surface

    def _register_interaction_surfaces(self, test_mode):
        """
        Registers all the notification surfaces

        :param test_mode: class instance created for test purposes, some
        features are disabled
        :type test_mode: bool

        """
        running_on_pythonanywhere = self._config_service.get_config("running_on_pythonanywhere_free", throw_error=False)

        # NotifyAdmin surface
        self._surfaces[GlobalBag.SURFACE_NOTIFY_ADMIN] = TelegramNotifyAdminSurface(
            GlobalBag.SURFACE_NOTIFY_ADMIN,
            self._config_service.get_config("telegram_notifyadmin_authorization_token"),
            self._config_service.get_config("telegram_notifyadmin_chat_id"),
            running_on_pythonanywhere=running_on_pythonanywhere,
            test_mode=test_mode
        )

        # Telegram bot Lurch
        self._surfaces[GlobalBag.SURFACE_TELEGRAM_BOT_LURCH] = TelegramSurface(
            GlobalBag.SURFACE_TELEGRAM_BOT_LURCH,
            self._config_service.get_config("telegram_lurch_authorization_token"),
            self._config_service.get_config("base_vps_address") + self._config_service.get_config("telegram_lurch_webhook_url_relative"),
            running_on_pythonanywhere=running_on_pythonanywhere,
            test_mode=test_mode
        )

    def _send_message(self, message):
        """
        Sends a message to one of the interaction surfaces.

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


