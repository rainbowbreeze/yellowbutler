"""
A surface to notify an admin about a particular message

Right now, it is a Telegram bot, but can be customized
"""
from yellowbot.surfaces.notifyadminsurface import NotifyAdminSurface
from yellowbot.surfaces.surfacemessage import SurfaceMessage
from yellowbot.surfaces.telegramsurface import TelegramSurface


class TelegramNotifyAdminSurface(NotifyAdminSurface, TelegramSurface):
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
        NotifyAdminSurface.__init__(self, surface_name, chat_id)
