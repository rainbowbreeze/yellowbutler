"""
Class to interact with Telegram surface
"""
import telepot
import urllib3

from yellowbot.surfaces.baseinteractionsurface import BaseInteractionSurface
from yellowbot.surfaces.surfacemessage import SurfaceMessage


class TelegramSurface(BaseInteractionSurface):
    """
    Allow YellowBot to interact with Telegram.

    Each instance of this class correspond to a bot managed in Telegram

    Even if there are multiple bots, the logic to manage then is all
     centralised in one YellowBot: think bots and "limited" instances of
     YellowBot, that have their own names and configurations in Telegram,
     but all bring to the same "brain" under the hood
    """

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
        :param auth_token: Telegram authorization token for the connected bot
        :param webhook_url: webhook url for the connected bot
        :param running_on_pythonanywhere: the whole app is running locally, so no need
        to set
        :param test_mode: class instance created for test purposes, some
        features are disabled
        """
        BaseInteractionSurface.__init__(self, surface_name)
        # Initialise and interact with Telegram only if not in test mode
        if not test_mode:
            self._init_pythonanywhere(running_on_pythonanywhere)
            self.telegram_bot = telepot.Bot(auth_token)
            self._set_webhook(webhook_url)

    def send_message(self, message):
        if not message:
            return

        return self.telegram_bot.sendMessage(message.channel_id, message.text)

    def _init_pythonanywhere(self, running_on_pythonanywhere):
        """
        Call it once to initialize Telegram library to interact with
         PythonAnywhere

        :param running_on_pythonanywhere: if the whole app is hosted and
        running on PythonAnywhere
        :return:
        """
        # If run in production (so, not run locally), sets the PythonAnywhere
        #  special config and the webhook for the bot.
        #  Otherwise, as soon as there is call to set the webhook when Flask
        #  is running locally, the command fails because of the proxy settings
        #  with urllib3.exceptions.ProxyError
        if running_on_pythonanywhere:
            return

        # You can leave this bit out if you're using a paid PythonAnywhere account
        proxy_url = "http://proxy.server:3128"
        telepot.api._pools = {
            'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
        }
        telepot.api._onetime_pool_spec = (
            urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))
        # end of the stuff that's only needed for free accounts

    def _set_webhook(self, new_webhook_url):
        """
        Sets the bot webhook url
        :param new_webhook_url:
        :return:
        """

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
            self.telegram_bot.setWebhook(
                new_webhook_url,
                max_connections=1)

    @staticmethod
    def from_telegram_update_to_message(surface_name, update):
        """
        Transform a Telegram update in a SurfaceMessage

        :param surface_name: the telegram bot that originated the update
        :param update: the Telegram update
        :return:
        """
        if "message" in update:
            text = update["message"]["text"]
            chat_id = update["message"]["chat"]["id"]
            message = SurfaceMessage(surface_name, chat_id, text)
            return message
        else:
            return None
