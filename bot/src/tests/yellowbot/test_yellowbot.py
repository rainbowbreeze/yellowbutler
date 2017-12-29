"""
Tests YellowBot basic features
"""
from unittest import TestCase

import os

from yellowbot.globalbag import GlobalBag
from yellowbot.surfaces.baseinteractionsurface import BaseInteractionSurface
from yellowbot.surfaces.surfacemessage import SurfaceMessage
from yellowbot.yellowbot import YellowBot


class TestYellowBot(TestCase):
    def setUp(self):
        """
        Tests if authorization works, providing a mock configuration files
         with authorized keys
        """
        # The file is under the same directory of this test class
        config_path = os.path.join(os.path.dirname(__file__), "yellowbot_config_test.json")
        self._yellowbot = YellowBot(config_file=config_path, test_mode=True)
        self._test_surface = FakeInteractionSurface()
        assert self._yellowbot.add_interaction_surface(self._test_surface)

    def tearDown(self):
        pass

    def test_isAuthorized(self):
        assert not self._yellowbot.is_client_authorized(None)
        assert not self._yellowbot.is_client_authorized("Random key")
        assert self._yellowbot.is_client_authorized("test_key_1")
        assert self._yellowbot.is_client_authorized("test_key_2")
        assert not self._yellowbot.is_client_authorized("test_key_3")

    def test_messageGearAsIntent(self):
        assert "My message" == self._yellowbot.process_intent(
            GlobalBag.ECHO_MESSAGE_INTENT,
            {GlobalBag.ECHO_MESSAGE_PARAM_MESSAGE:"My message"})

        assert "" == self._yellowbot.process_intent(
            GlobalBag.ECHO_MESSAGE_INTENT,
            {GlobalBag.ECHO_MESSAGE_PARAM_MESSAGE:""})

    def test_messageGearAsMessage(self):
        message = SurfaceMessage(
            FakeInteractionSurface.SURFACE_ID,
            "Test_Channel",
            "Echo My message")
        self._yellowbot.receive_message(message)
        assert "My message" == self._test_surface.last_message


class FakeInteractionSurface(BaseInteractionSurface):
    """
    Surface to check if messages have really been sent
    """
    SURFACE_ID = "Test_Surface"

    def __init__(self):
        BaseInteractionSurface.__init__(self, FakeInteractionSurface.SURFACE_ID)
        self.last_message = None

    def send_message(self, message):
        self.last_message = message.text
