"""
Test for SendMessageGear
"""
from unittest import TestCase

from tests.yellowbot.surfaces.fakeinteractionsurface import FakeInteractionSurface
from yellowbot.configservice import ConfigService
from yellowbot.gears.sendmessagegear import SendMessageGear
from yellowbot.globalbag import GlobalBag


class TestSendMessageGear(TestCase):
    def setUp(self):
        self._config_service = ConfigService("../tests/yellowbot/yellowbot_config_test.json")
        self._gear = SendMessageGear(self._config_service, True)

        self._test_surface = FakeInteractionSurface(FakeInteractionSurface.SURFACE_ID)
        # Add a test interaction surface
        self._gear.add_interaction_surface(
            FakeInteractionSurface.SURFACE_ID,
            self._test_surface)

    def tearDown(self):
        pass

    def test_process_intent(self):
        self.assertIsNone(self._test_surface.last_message)

        # TODO check the various missing parameters condition

        surface_id = FakeInteractionSurface.SURFACE_ID
        channel_id = "Test_channel_id"
        text = "Test text"
        result = self._gear.process_intent(
            GlobalBag.SEND_MESSAGE_INTENT,
            {
                GlobalBag.SEND_MESSAGE_PARAM_SURFACE_ID: surface_id,
                GlobalBag.SEND_MESSAGE_PARAM_CHANNEL_ID: channel_id,
                GlobalBag.SEND_MESSAGE_PARAM_TEXT: text
            }
        )

        self.assertIsNotNone(result)
        self.assertTrue(result.went_well())
        self.assertTrue(result.has_messages())
        messages = result.get_messages()
        self.assertEqual(1, len(messages))
        self.assertEqual(FakeInteractionSurface.RETURN_TEST, messages[0])
        self.assertEqual(surface_id, self._test_surface.last_message.surface_id)
        self.assertEqual(channel_id, self._test_surface.last_message.channel_id)
        self.assertEqual(text, self._test_surface.last_message.text)
