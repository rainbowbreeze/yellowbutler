"""
Tests YellowBot basic features
"""
from unittest import TestCase
from yellowbot.yellowbot import YellowBot


class TestYellowBot(TestCase):

    def test_is_authorized(self):
        yb = YellowBot()

        assert not yb.is_authorized(None)

