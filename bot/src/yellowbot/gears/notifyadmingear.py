"""
Gear to notify administrator about something that has happened
"""

from yellowbot.gears.basegear import BaseGear
from yellowbot.globalbag import GlobalBag
from yellowbot.loggingservice import LoggingService
from yellowbot.surfaces.telegramnotifyadminsurface import TelegramNotifyAdminSurface


class NotifyAdminGear(BaseGear):
    """
    """
    INTENTS = [GlobalBag.NOTIFY_ADMIN_INTENT]
    PARAM_MESSAGE = GlobalBag.NOTIFY_ADMIN_PARAM_MESSAGE

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
        BaseGear.__init__(self, NotifyAdminGear.__name__, self.INTENTS)
        self._config_service = config_service
        self._logger = LoggingService.get_logger(__name__)

        running_on_pythonanywhere = self._config_service.get_config("running_on_pythonanywhere_free", throw_error=False)

        # Registers the interaction surface
        self._admin_surface = TelegramNotifyAdminSurface(
            GlobalBag.SURFACE_NOTIFY_ADMIN,
            self._config_service.get_config("telegram_notifyadmin_authorization_token"),
            self._config_service.get_config("telegram_notifyadmin_chat_id"),
            running_on_pythonanywhere=running_on_pythonanywhere,
            test_mode=test_mode
        )

    def process_intent(self, intent, params):
        """
        Right now, call YellowBot to send a message, using its configuration

        :param intent:
        :param params:
        :return:
        """
        if NotifyAdminGear.INTENTS[0] != intent:
            message = "Call to {} using wrong intent {}".format(__name__, intent)
            self._logger.info(message)
            return message
        if NotifyAdminGear.PARAM_MESSAGE not in params:
            return "Missing {} parameter in the request".format(NotifyAdminGear.PARAM_MESSAGE)

        text = params[NotifyAdminGear.PARAM_MESSAGE]
        self._logger.info("Notify admin about {}".format(text))

        # Creates a new message and dispatch it
        message = self._admin_surface.forge_notification(text)
        return self._admin_surface.send_message(message)

    def swap_surface_for_test(self, new_surface):
        """
        Changes the surface for test purposes
        :param new_surface:
        :return:
        """
        self._admin_surface = new_surface

