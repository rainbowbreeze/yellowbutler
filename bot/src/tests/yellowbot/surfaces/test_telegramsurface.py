"""
Tests TelegramSurface class
"""
from unittest import TestCase

from yellowbot.surfaces.telegramsurface import TelegramSurface


class TestTelegramSurface(TestCase):
    def setUp(self):
        self.surface = TelegramSurface(
            "Telegram-UnitTest",
            "Fake_auth_token",
            "Fake_webhook_url",
            test_mode=True)

    def tearDown(self):
        pass
