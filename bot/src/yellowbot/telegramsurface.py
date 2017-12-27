"""
Class to interact with Telegram surface
"""

from yellowbot.yellowbot import YellowBot
import telepot
import urllib3


class TelegramSurface:
    """
    Allow YellowBot to interact with Telegram
    """
    def __init__(self, yellowbot):
        self.yellowbot = yellowbot
        # Reads the Telegram auth token from configuration
        self.telegram_bot = telepot.Bot(self.yellowbot.get_config("telegram_authorization_token"))
        self._init_pythonanywhere()
        self._set_webhook()

    def _init_pythonanywhere(self):
        """
        Call it once to initialize Telegram library to interact with
         PythonAnywhere

        :return:
        """
        # If run in production (so, not run locally), sets the PythonAnywhere
        #  special config and the webhook for the bot.
        #  Otherwise, as soon as there is call to set the webhook when Flask
        #  is running locally, the command fails because of the proxy settings
        running_locally = self.yellowbot.get_config("running_locally", throw_error=False)
        if running_locally:
            return

        # You can leave this bit out if you're using a paid PythonAnywhere account
        proxy_url = "http://proxy.server:3128"
        telepot.api._pools = {
            'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
        }
        telepot.api._onetime_pool_spec = (
            urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))
        # end of the stuff that's only needed for free accounts

    def _set_webhook(self):
        # Sets the webhook url, reading it from configuration
        # Sometimes there is an exception
        #    telepot.exception.TooManyRequestsError: ('Too Many Requests: retry after 1', 429 ...
        #  It's because there is a limit on how often the webhook is set.
        #  In order to avoid it, follow https://github.com/nickoala/telepot/issues/165#issuecomment-256056446
        #  TL;DR: check if the webhook needs to be changed, before changing it
        # If there is an exception because the proxy cannot be reached, is
        #  because the PythonAnyWhere configurations: don't do them
        webhook_info = self.telegram_bot.getWebhookInfo()
        new_webhook_url = self.yellowbot.get_config('telegram_webhook_url')
        # With get, it also checks for the existence of the key in the dict.
        #  If it doesn't exists, return None
        if webhook_info.get('url') != new_webhook_url:
            self.telegram_bot.setWebhook(
                new_webhook_url,
                max_connections=1)

    def process_update(self, update):
        """
        Process an update message from Telegram. It is what hits the webhook

        :param: update
        :return:
        """
        if "message" in update:
            text = update["message"]["text"]
            chat_id = update["message"]["chat"]["id"]
            # chat_response = self._process_chat_message(text)
            self._send_chat_message(chat_id, "You said '{}'".format(text))

    def _process_chat_message(self, message):
        """
        Process a generic message from Telegram
        :param message:
        :return:
        """

        intent, params = self.yellow_bot.infer_intent_and_params(message)
        return self.yellow_bot.echo_message(message)

    def _send_chat_message(self, chat_id, param):
        """
        Send a message to Telegram
        :param chat_id:
        :param param:
        :return:
        """
        self.telegram_bot.sendMessage(chat_id, param)
        pass
