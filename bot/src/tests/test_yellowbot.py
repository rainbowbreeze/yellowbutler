from unittest import TestCase
from yellowbot.yellowbot import YellowBot


class TestYellowButler(TestCase):
    def test_is_security_code_valid(self):
        yb = YellowBot()

        code1 = "test_code_1"
        code2 = "test_code_2"
        code3 = "test_code_3"

        # No codes
        if yb.is_security_code_valid(code1):
            self.fail("Unknown code1 authorized")
        if yb.is_security_code_valid(code2):
            self.fail("Unknown code2 authorized")

        # Fist code added
        yb.append_security_key(code1)
        if not yb.is_security_code_valid(code1):
            self.fail("Known code1 non-authorized")
        if yb.is_security_code_valid(code2):
            self.fail("Unknown code2 authorized")

        # Second code added
        yb.append_security_key(code2)
        if not yb.is_security_code_valid(code1):
            self.fail("Known code1 non-authorized")
        if not yb.is_security_code_valid(code2):
            self.fail("Known code2 non-authorized")
