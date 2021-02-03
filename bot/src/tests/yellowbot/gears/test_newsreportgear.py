"""
Test NewsReport gear
"""

from unittest import TestCase
import responses
import os
import arrow

from yellowbot.gears.newsreportergear import NewsReportGear
from yellowbot.globalbag import GlobalBag

class TestNewsReportGear(TestCase):
    def setUp(self):
        self._gear = NewsReportGear()

    def tearDown(self):
        pass

    def test_youtube(self):
        result = self._gear._analize_youtube_channel('')
        self.assertEqual(2, len(result))

