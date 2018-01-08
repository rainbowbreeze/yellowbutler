"""
Class to interact with Telegram surface
"""
import logging

import telepot
import urllib3

from yellowbot.loggingservice import LoggingService
from yellowbot.surfaces.baseinteractionsurface import BaseInteractionSurface
from yellowbot.surfaces.surfacemessage import SurfaceMessage


class TelegramSurface(BaseInteractionSurface):
    """
    Allow YellowBot to interact with Telegram.

    Each instance of this class correspond to a bot managed in Telegram

    Even if there are multiple bots, the logic to manage then is all
     centralised in one YellowBot: think bots and "limited" instances of
     YellowBot, that have their own names and configurations in Telegram,
     but are all part of the same "brain" under the hood
    """

    # Define if fixes for various environments have been applied
    _FIX_ConnectionResetError_APPLIED = False
    _FIX_PythonAnywhereFree_APPLIED = False

    def __init__(self,
                 surface_name,
                 auth_token,
                 webhook_url,
                 running_on_pythonanywhere=False,
                 test_mode=False):
        """
        Create the surface and initialize the elements

        :param surface_name: a name that identify uniquely the Telegram bot
        connected with this surface instance
        :type surface_name: str

        :param auth_token: Telegram authorization token for the connected bot
        :type auth_token: str

        :param webhook_url: webhook url for the connected bot
        :type webhook_url: str

        :param running_on_pythonanywhere: the whole app is running locally, so no need
        to set
        :type running_on_pythonanywhere: bool

        :param test_mode: class instance created for test purposes, some
        features are disabled
        :type test_mode: bool
        """
        BaseInteractionSurface.__init__(self, surface_name)
        # Initialise and interact with Telegram only if not in test mode
        self._logger = LoggingService.get_logger(__name__)

        self._test_mode = test_mode
        if not self._test_mode:
            self._fix_connection_reset_error()
            self._init_pythonanywhere(running_on_pythonanywhere)
            self.telegram_bot = telepot.Bot(auth_token)
            self._set_webhook(webhook_url)

    def send_message(self, message):
        # Do not send empty message or message while testing
        if not message or self._test_mode:
            return
        return self.telegram_bot.sendMessage(message.channel_id, message.text)

    def _init_pythonanywhere(self, running_on_pythonanywhere_free):
        """
        Call it once to initialize Telegram library to interact with
         PythonAnywhere

        :param running_on_pythonanywhere_free: if the whole app is hosted and
        running on PythonAnywhere with free account
        :return:
        """
        # If run in production (so, not run locally), sets the PythonAnywhere
        #  special config and the webhook for the bot.
        #  Otherwise, as soon as there is call to set the webhook when Flask
        #  is running locally, the command fails because of the proxy settings
        #  with urllib3.exceptions.ProxyError
        if not running_on_pythonanywhere_free:
            return

        if TelegramSurface._FIX_PythonAnywhereFree_APPLIED:
            return

        self._logger.info("Applying PythonAnywhere Free fix")

        # You can leave this bit out if you're using a paid PythonAnywhere account
        # https://help.pythonanywhere.com/pages/403ForbiddenError/
        proxy_url = "http://proxy.server:3128"
        telepot.api._pools = {
            'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
        }
        telepot.api._onetime_pool_spec = (
            urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))
        # end of the stuff that's only needed for free accounts

        TelegramSurface._FIX_PythonAnywhereFree_APPLIED = True

    def _fix_connection_reset_error(self):
        """
        Tries to fix ConnectionResetError: [Errno 104] Connection reset by peer.
        It happens first time a request is sent to the bot via Telegram,
         and the bot doesn't reply, but the request is processed. Simply,
         the telepot library is unable to send a reply to Telegram

        Reference on https://github.com/nickoala/telepot/issues/87#issuecomment-235173302

        I tried different combos for the settings (telepot.api._pools,
         force_independent_connection and _onetime_pool_spec) and it seems
         that only force_independent_connection is required to solve the issue
        I'm leaving the code commented for future references and (hopefully
          not) future issues

        :return:
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

    def _set_webhook(self, new_webhook_url):
        """
        Sets the bot webhook url
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
    def from_telegram_update_to_message(surface_name, update):
        """
        Transform a Telegram update in a SurfaceMessage

        :param surface_name: the telegram bot that originated the update
        :type surface_name: str

        :param update: the Telegram update
        :type update: dict

        :return: The message generated from the update, otherwise None if
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
    def from_telegram_update_to_auth_key(update):
        """
        From a Telegram update, generates the authorization key

        :param update: the Telegram update
        :type update: dict

        :return: the authorization code generated
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

