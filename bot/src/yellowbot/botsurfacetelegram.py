"""
Class to interact with Telegram surface
"""

from yellowbot import YellowBot

class BotSurfaceTelegram:
    """
    Allow YellowBot to interact with Telegram
    """
    def __init__(self):
        self.yellow_bot = YellowBot()
        pass

    def process_chat_message(self, message):
        """
        Process a generic message from Telegram
        :param message:
        :return:
        """

        intent, params = self.yellow_bot.infer_intent_and_params(message)
        return self.yellow_bot.echo_message(message)
