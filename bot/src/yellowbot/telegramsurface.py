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
        self.telegram_bot = telepot.Bot('YOUR_AUTHORIZATION_TOKEN')

    def init_python_anywhere(self):
        """
        Call it once to initialize Telegram library to interact with
         PythonAnywhere

        :return:
        """
        # You can leave this bit out if you're using a paid PythonAnywhere account
        proxy_url = "http://proxy.server:3128"
        telepot.api._pools = {
            'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
        }
        telepot.api._onetime_pool_spec = (
        urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))
        # end of the stuff that's only needed for free accounts


    def process_chat_message(self, message):
        """
        Process a generic message from Telegram
        :param message:
        :return:
        """

        intent, params = self.yellow_bot.infer_intent_and_params(message)
        return self.yellow_bot.echo_message(message)

    def send_chat_message(self, chat_id, param):
        """
        Send a message to Telegram
        :param chat_id:
        :param param:
        :return:
        """
        self.telegram_bot.sendMessage(chat_id, param)
        pass
