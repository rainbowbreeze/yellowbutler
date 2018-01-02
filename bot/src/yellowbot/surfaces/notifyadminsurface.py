"""
A surface to notify an admin about a particular message

Right now, it is a Telegram bot, but can be customized
"""
from yellowbot.surfaces.baseinteractionsurface import BaseInteractionSurface
from yellowbot.surfaces.surfacemessage import SurfaceMessage


class NotifyAdminSurface(BaseInteractionSurface):
    def __init__(self,
                 surface_name,
                 channel_id):
        BaseInteractionSurface.__init__(
            self,
            surface_name)
        self._channel_id = channel_id

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
            self._channel_id,
            text
        )
