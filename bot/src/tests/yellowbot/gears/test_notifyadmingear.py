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
        assert self._test_surface.last_message is None

        # TODO check the various missing parameters condition

        text = "Test notify admin text"
        result = self._gear.process_intent(
            GlobalBag.NOTIFY_ADMIN_INTENT,
            {
                GlobalBag.NOTIFY_ADMIN_PARAM_MESSAGE: text
            }
        )

        assert FakeNotifyAdminInteractionSurface.RETURN_TEST == result
        assert GlobalBag.SURFACE_NOTIFY_ADMIN == self._test_surface.last_message.surface_id
        assert "Notify_Test_Channel" == self._test_surface.last_message.channel_id
        assert text == self._test_surface.last_message.text
