"""
Tests YellowBot basic features
"""
from unittest import TestCase
from yellowbot.yellowbot import YellowBot


class TestYellowBot(TestCase):

    def test_is_security_code_valid(self):
        yb = YellowBot()

