"""
Tests YellowBot basic features
"""
from unittest import TestCase

import os

from yellowbot.yellowbot import YellowBot


class TestYellowBot(TestCase):

    def test_is_authorized(self):
        config_path = os.path.join(os.path.dirname(__file__), "yellowbotconfig_test.json")
        yb = YellowBot(config_file=config_path)

        assert not yb.is_client_authorized(None)
        assert not yb.is_client_authorized("Random key")
        assert yb.is_client_authorized("test_key_1")
        assert yb.is_client_authorized("test_key_2")
        assert not yb.is_client_authorized("test_key_3")


