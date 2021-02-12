"""
Test for NotifyAdminGear
"""
from unittest import TestCase

from tests.yellowbot.surfaces.fakeinteractionsurface import FakeInteractionSurface
from tests.yellowbot.surfaces.fakenotifyadmininteractionsurface import FakeNotifyAdminInteractionSurface
from yellowbot.configservice import ConfigService
from yellowbot.gears.notifyadmingear import NotifyAdminGear
from yellowbot.globalbag import GlobalBag


class TestNotifyAdminGear(TestCase):
    def setUp(self):
        self._config_service = ConfigService("../tests/yellowbot/yellowbot_config_test.json")
        self._test_surface = FakeNotifyAdminInteractionSurface(
            GlobalBag.SURFACE_NOTIFY_ADMIN,
            "Notify_Test_Channel"
        )
        self._gear = NotifyAdminGear(self._config_service, True)
        # Add a test interaction surface
        self._gear.swap_surface_for_test(self._test_surface)

    def tearDown(self):
        pass

    def test_process_intent(self):
        self.assertIsNone(self._test_surface.last_message)

        # TODO check the various missing parameters condition

        text = "Test notify admin text"
        result = self._gear.process_intent(
            GlobalBag.NOTIFY_ADMIN_INTENT,
            {
                GlobalBag.NOTIFY_ADMIN_PARAM_MESSAGE: text
            }
        )

        self.assertIsNotNone(result)
        self.assertTrue(result.went_well())
        self.assertTrue(result.has_messages())
        messages = result.get_messages()
        self.assertEqual(1, len(messages))
        self.assertEqual(FakeNotifyAdminInteractionSurface.RETURN_TEST, messages[0])
        self.assertEqual(GlobalBag.SURFACE_NOTIFY_ADMIN, self._test_surface.last_message.surface_id)
        self.assertEqual("Notify_Test_Channel", self._test_surface.last_message.channel_id)
        self.assertEqual(text, self._test_surface.last_message.text)

