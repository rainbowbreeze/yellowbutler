"""Gear to notify administrator about something that has happened
"""

from typing import Any, ClassVar, Dict, List, Optional, TypeVar

from yellowbot.configservice import ConfigService
from yellowbot.gears.basegear import BaseGear
from yellowbot.gears.gearexecutionresult import GearExecutionResult
from yellowbot.globalbag import GlobalBag
from yellowbot.loggingservice import LoggingService
from yellowbot.surfaces.notifyadminsurface import NotifyAdminSurface
from yellowbot.surfaces.telegramnotifyadminsurface import TelegramNotifyAdminSurface

# See here for explanation: https://www.python.org/dev/peps/pep-0484/#the-type-of-class-objects
NAS = TypeVar('NAS', bound=NotifyAdminSurface)

class NotifyAdminGear(BaseGear):
    """
    """
    INTENTS: ClassVar[List[str]] = [GlobalBag.NOTIFY_ADMIN_INTENT]
    PARAM_MESSAGE: ClassVar[str] = GlobalBag.NOTIFY_ADMIN_PARAM_MESSAGE

    def __init__(
        self,
        config_service: ConfigService,
        test_mode: bool = False
    ) -> None:
        """Init the class

        :param config_service: configuration service
        :type config_service: ConfigService

        :param test_mode: class instance created for test purposes, some
        features are disabled
        :type test_mode: bool
        """
        super().__init__(self.__class__.__name__, self.INTENTS)
        self._config_service = config_service
        self._logger = LoggingService.get_logger(__name__)

        # Registers the interaction surface
        self._admin_surface = TelegramNotifyAdminSurface(
            GlobalBag.SURFACE_NOTIFY_ADMIN,
            self._config_service.get_config("telegram_notifyadmin_authorization_token"),
            self._config_service.get_config("telegram_notifyadmin_chat_id"),
            test_mode=test_mode
        )

    def process_intent(
        self,
        intent: str,
        params: Dict[str, Any]
    ) -> GearExecutionResult:
        """Calls YellowBot to send a message, using its configuration

        :param intent:
        :param params:
        :return:
        """

        err_message = None
        if NotifyAdminGear.INTENTS[0] != intent:
            err_message = "Call to {} using wrong intent {}".format(__name__, intent)
        if NotifyAdminGear.PARAM_MESSAGE not in params:
            err_message = "Missing {} parameter in the request".format(NotifyAdminGear.PARAM_MESSAGE)
        if err_message:
            self._logger.info(err_message)
            return GearExecutionResult.ERROR(err_message)

        text = params[NotifyAdminGear.PARAM_MESSAGE]
        self._logger.info("Notify admin about {}".format(text))

        # Creates a new message and dispatch it
        message = self._admin_surface.forge_notification(text)
        return GearExecutionResult.OK(self._admin_surface.send_message(message))

    def swap_surface_for_test(
        self,
        new_admin_surface: NAS
    ) -> None:
        """Changes the surface for test purposes

        :param new_admin_surface:
        :type new_admin_surface: NotifyAdminSurface

        """

        self._admin_surface = new_admin_surface
