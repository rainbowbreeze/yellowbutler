"""
A surface to notify an admin about a particular message

Right now, it is a Telegram bot, but can be customized
"""
from yellowbot.surfaces.surfacemessage import SurfaceMessage
from yellowbot.surfaces.telegramsurface import TelegramSurface


class NotifyAdminSurface(TelegramSurface):
    def __init__(self,
                 surface_name,
                 auth_token,
                 chat_id,
                 running_on_pythonanywhere,
                 test_mode=False):
        TelegramSurface.__init__(
            self,
            surface_name,
            auth_token,
            webhook_url="",
            running_on_pythonanywhere=running_on_pythonanywhere,
            test_mode=test_mode)
        self._chat_id = chat_id

    def forge_notification(self, text):
        """
        Creates the notification message, in a way coherent with the surface
         capabilities

        :param text:
        :type text: str

        :return: the message to send
        :rtype: SurfaceMessage
        """
        return SurfaceMessage(
            self._surface_name,
            self._chat_id,
            text
        )
