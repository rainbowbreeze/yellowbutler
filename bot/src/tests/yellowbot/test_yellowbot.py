"""
Tests YellowBot basic features
"""
from unittest import TestCase

import os

from yellowbot.globalbag import GlobalBag
from yellowbot.yellowbot import YellowBot


class TestYellowBot(TestCase):

    def setUp(self):
        """
        Tests if authorization works, providing a mock configuration files
         with authorized keys
        """
        # The file is under the same directory of this test class
        config_path = os.path.join(os.path.dirname(__file__), "yellowbotconfig_test.json")
        self.yb = YellowBot(config_file=config_path, test_mode=True)

    def tearDown(self):
        pass

    def test_isAuthorized(self):
        assert not self.yb.is_client_authorized(None)
        assert not self.yb.is_client_authorized("Random key")
        assert self.yb.is_client_authorized("test_key_1")
        assert self.yb.is_client_authorized("test_key_2")
        assert not self.yb.is_client_authorized("test_key_3")

    def test_echoMessageGear(self):
        assert "My message" == self.yb.process_intent(
            GlobalBag.ECHO_MESSAGE_INTENT,
            {GlobalBag.ECHO_MESSAGE_PARAM_MESSAGE:"My message"})

        assert "" == self.yb.process_intent(
            GlobalBag.ECHO_MESSAGE_INTENT,
            {GlobalBag.ECHO_MESSAGE_PARAM_MESSAGE:""})


