"""Class to interact with Telegram surface
"""

from typing import ClassVar, Optional

import telepot

from yellowbot.loggingservice import LoggingService
from yellowbot.surfaces.baseinteractionsurface import BaseInteractionSurface
from yellowbot.surfaces.surfacemessage import SurfaceMessage


class TelegramSurface(BaseInteractionSurface):
    """Allow YellowBot to interact with Telegram.

    Each instance of this class correspond to a bot managed in Telegram

    Even if there are multiple bots, the logic to manage them is all
     centralised in one YellowBot: think bots and "limited" instances of
     YellowBot, that have their own names and configurations in Telegram,
     but are all part of the same "brain" under the hood
    """

    # Define if fixes for various environments have been applied, as class variable with ClassVar
    _FIX_ConnectionResetError_APPLIED: ClassVar[bool] = False
    _FIX_PythonAnywhereFree_APPLIED: ClassVar[bool] = False

    def __init__(
        self,
        surface_name: str,
        auth_token: str,
        webhook_url: str,
        test_mode:bool = False
    ) -> None:
        """Create the surface and initialize the elements

        :param surface_name: a name that identify uniquely the Telegram bot
        connected with this surface instance
        :type surface_name: str

        :param auth_token: Telegram authorization token for the connected bot
        :type auth_token: str

        :param webhook_url: webhook url for the connected bot
        :type webhook_url: str

        :param test_mode: class instance created for test purposes, some
        features are disabled
        :type test_mode: bool
        """

        super().__init__(surface_name)
        # Initialise and interact with Telegram only if not in test mode
        self._logger = LoggingService.get_logger(__name__)

        self._test_mode = test_mode
        if not self._test_mode:
            self._fix_connection_reset_error()
            self.telegram_bot = telepot.Bot(auth_token)
            self._set_webhook(webhook_url)

    def send_message(self, message: SurfaceMessage) -> Optional[str]:
        """Send a message to Telegram

        :returns: the message_id returned by Telegram once the message is sent
        :rtype: str
        """

        # Do not send empty message or message while testing
        if self._test_mode:
            return "Message not really sent in test mode"
        if not message:
            return None

        # Sometimes an error happens sending a message with only a _
        #  like "Missing city_name parameter in the request"
        #  and the entire sendMessage call crashes
        # To check Markdown, please refer to https://core.telegram.org/bots/api#sendmessage
        try:
            return_message = self.telegram_bot.sendMessage(message.channel_id, message.text, "Markdown")
        except BaseException as err:
            return_message = self.telegram_bot.sendMessage(message.channel_id, message.text)

        # It returns a string with the message id, not the whole message object
        return str(return_message["message_id"]) if "message_id" in return_message else None

    def _fix_connection_reset_error(self) -> None:
        """Tries to fix ConnectionResetError: [Errno 104] Connection reset by peer.
        It happens first time a request is sent to the bot via Telegram,
         and the bot doesn't reply, but the request is processed. Simply,
         the telepot library is unable to send a reply to Telegram

        Reference on https://github.com/nickoala/telepot/issues/87#issuecomment-235173302

        I tried different combos for the settings (telepot.api._pools,
         force_independent_connection and _onetime_pool_spec) and it seems
         that only force_independent_connection is required to solve the issue
        I'm leaving the code commented for future references and (hopefully
          not) future issues
        """

        if TelegramSurface._FIX_ConnectionResetError_APPLIED:
            return

        self._logger.info("Applying ConnectionResetError fix")

        # telepot.api._pools = {
        #     'default': urllib3.PoolManager(num_pools=3, maxsize=10, retries=3, timeout=30),
        # }

        def force_independent_connection(req, **user_kw):
            return None
        telepot.api._which_pool = force_independent_connection

        # telepot.api._onetime_pool_spec = (urllib3.PoolManager, dict(num_pools=1, maxsize=1, retries=3, timeout=30))

        TelegramSurface._FIX_ConnectionResetError_APPLIED = True

    def _set_webhook(self, new_webhook_url: str) -> None:
        """Sets the bot webhook url
        :param new_webhook_url: new webhook to register for the bot
        :type new_webhook_url: str
        """

        if self._test_mode or not new_webhook_url:
            return

        # Sometimes there is an exception
        #    telepot.exception.TooManyRequestsError: ('Too Many Requests: retry after 1', 429 ...
        #  It's because there is a limit on how often the webhook is set.
        #  In order to avoid it, follow https://github.com/nickoala/telepot/issues/165#issuecomment-256056446
        #  TL;DR: check if the webhook needs to be changed, before changing it
        # If there is an urllib3.exceptions.ProxyError error, is because the
        #  PythonAnyWhere configuration: don't do it
        webhook_info = self.telegram_bot.getWebhookInfo()
        # With get, it also checks for the existence of the key in the dict.
        #  If it doesn't exists, return None
        if webhook_info.get('url') != new_webhook_url:
            self._logger.info("Setting webhook to %s", new_webhook_url)
            self.telegram_bot.setWebhook(
                new_webhook_url,
                max_connections=2)
        else:
            self._logger.info("Webhook is already set to %s", webhook_info.get('url'))

    @staticmethod
    def from_telegram_update_to_message(
        surface_name: str,
        update: dict
    ) -> Optional[SurfaceMessage]:
        """Transform a Telegram update in a SurfaceMessage

        :param surface_name: the telegram bot that originated the update
        :type surface_name: str

        :param update: the Telegram update
        :type update: dict

        :returns: The message generated from the update, otherwise None if
        the update is not a text message
        :rtype: SurfaceMessage
        """
        try:
            if "message" in update:
                text = update["message"]["text"]
                chat_id = update["message"]["chat"]["id"]
                message = SurfaceMessage(surface_name, chat_id, text)
                return message
            else:
                return None
        except KeyError as e:
            return None

    @staticmethod
    def from_telegram_update_to_auth_key(update: dict) -> Optional[str]:
        """
        From a Telegram update, generates the authorization key

        :param update: the Telegram update
        :type update: dict

        :returns: the authorization code generated
        :rtype: str
        """

        try:
            if "message" in update:
                # Auth_key has to be a string, while id is an integer.
                #  Reference at https://core.telegram.org/bots/api#user
                return "{}".format(update["message"]["from"]["id"])
            else:
                return None
        except KeyError:
            # Wrong or missing fields
            return None
        except TypeError:
            # Wrong types in the fields
            return None
