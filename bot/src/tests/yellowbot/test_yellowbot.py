"""
Tests YellowBot basic features
"""
from unittest import TestCase

import os

from tests.yellowbot.surfaces.fakeinteractionsurface import FakeInteractionSurface
from yellowbot.globalbag import GlobalBag
from yellowbot.surfaces.notifyadminsurface import NotifyAdminSurface
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

    def tearDown(self):
        pass

    def test_noConfigFileExceptionRaised(self):
        with self.assertRaises(ValueError):
            YellowBot(config_file="non_existing_file.json")

    def test_isAuthorized(self):
        assert not self._yellowbot.is_client_authorized(None)
        assert not self._yellowbot.is_client_authorized("Random key")
        assert self._yellowbot.is_client_authorized("test_key_1")
        assert self._yellowbot.is_client_authorized("test_key_2")
        assert not self._yellowbot.is_client_authorized("test_key_3")

    def test_processIntentWithEchoMessageGear(self):
        assert "My message" == self._yellowbot.process_intent(
            GlobalBag.ECHO_MESSAGE_INTENT,
            {GlobalBag.ECHO_MESSAGE_PARAM_MESSAGE:"My message"})

        assert "" == self._yellowbot.process_intent(
            GlobalBag.ECHO_MESSAGE_INTENT,
            {GlobalBag.ECHO_MESSAGE_PARAM_MESSAGE:""})

    def test_receiveMessageForEchoMessageGear(self):
        message = SurfaceMessage(
            FakeInteractionSurface.SURFACE_ID,
            "Test_Channel",
            "Echo My message")
        self._yellowbot.receive_message(message)
        assert "Test_Channel" == self._test_surface.last_message.channel_id
        assert "My message" == self._test_surface.last_message.text

    def test_notifyAdmin(self):
        # Mock the notify admin surface
        notify_surface = FakeNotifyAdminInteractionSurface(GlobalBag.SURFACE_NOTIFY_ADMIN, "Notify_Test")
        self._yellowbot.add_interaction_surface(GlobalBag.SURFACE_NOTIFY_ADMIN, notify_surface)
        self._yellowbot.notify_admin("Test notification message")
        # Nothing in the other interaction surfaces
        assert None == self._test_surface.last_message
        # And the right message in mocked the notify admin surface
        assert "Notify_Test" == notify_surface.last_message.channel_id
        assert "Test notification message" == notify_surface.last_message.text


class FakeNotifyAdminInteractionSurface(NotifyAdminSurface):
    """
    Surface to check if messages have really been sent
    Cannot call it TestInteractionSurface, otherwise tests will be execute
     on this class too
    """
    SURFACE_ID = "Test_Surface"

    def __init__(self, surface_id, channel_id):
        """
        Test surface

        :param surface_id: id of the surface to use
        :type surface_id: str
        """
        NotifyAdminSurface.__init__(self, surface_id, channel_id)
        self.last_message = None

    def send_message(self, message):
        self.last_message = message
