"""
A surface to notify an admin about a particular message

Right now, it is a Telegram bot, but can be customized
"""
from yellowbot.surfaces.notifyadminsurface import NotifyAdminSurface
from yellowbot.surfaces.telegramsurface import TelegramSurface


class TelegramNotifyAdminSurface(NotifyAdminSurface, TelegramSurface):
    def __init__(self,
                 surface_name,
                 auth_token,
                 chat_id,
                 test_mode=False):
        NotifyAdminSurface.__init__(self, surface_name, chat_id)
        TelegramSurface.__init__(
            self,
            surface_name,
            auth_token,
            webhook_url="",
            test_mode=test_mode)
