"""
Tests YellowBot basic features
"""
from unittest import TestCase

import os

from tests.yellowbot.surfaces.fakeinteractionsurface import FakeInteractionSurface
from yellowbot.globalbag import GlobalBag
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
        self.assertFalse(self._yellowbot.is_client_authorized(None))
        self.assertFalse(self._yellowbot.is_client_authorized("Random key"))
        self.assertTrue(self._yellowbot.is_client_authorized("test_key_1"))
        self.assertTrue(self._yellowbot.is_client_authorized("test_key_2"))
        self.assertFalse(self._yellowbot.is_client_authorized("test_key_3"))

    def test_processIntentWithEchoMessageGear(self):
        result = self._yellowbot.process_intent(
            GlobalBag.ECHO_MESSAGE_INTENT,
            {GlobalBag.ECHO_MESSAGE_PARAM_MESSAGE:"My message"})
        self.assertIsNotNone(result)
        self.assertTrue(result.went_well())
        self.assertTrue(result.has_messages())
        messages = result.get_messages()
        self.assertEqual(1, len(messages))
        self.assertEqual("My message", messages[0])

        result = self._yellowbot.process_intent(
            GlobalBag.ECHO_MESSAGE_INTENT,
            {GlobalBag.ECHO_MESSAGE_PARAM_MESSAGE: ""})
        self.assertIsNotNone(result)
        self.assertTrue(result.went_well())
        self.assertFalse(result.has_messages())

    def test_receiveMessageForEchoMessageGear(self):
        message = SurfaceMessage(
            FakeInteractionSurface.SURFACE_ID,
            "Test_Channel",
            "Echo My message")
        with self.assertRaises(ValueError):
            # Because the surface id is unknown, an exception is raised
            self._yellowbot.receive_message(message)
            assert "Test_Channel" == self._test_surface.last_message.channel_id
            assert "My message" == self._test_surface.last_message.text



