"""
Test ConfigService
"""
import os
from unittest import TestCase

from yellowbot.configservice import ConfigService


class TestConfigService(TestCase):
    def setUp(self):
        """
        Tests if authorization works, providing a mock configuration files
         with authorized keys
        """
        # The file is under the same directory of this test class
        config_path = os.path.join(os.path.dirname(__file__), "yellowbot_config_test.json")
        self._config_service = ConfigService(config_file=config_path)

    def tearDown(self):
        pass

    def test_noConfigFileExceptionRaised(self):
        with self.assertRaises(ValueError):
            ConfigService(config_file="non_existing_file.json")

    def test_get_config(self):
        #TODO write tests here
        pass

