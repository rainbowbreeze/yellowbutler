"""
Test CommitStrip gear
"""
from unittest import TestCase

import os

import arrow

from yellowbot.gears.commitstripgear import CommitStripGear
from yellowbot.globalbag import GlobalBag

TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), "commitstrip_example_{}.txt")


class TestCommitStripGear(TestCase):
    def setUp(self):
        self._gear = CommitStripGear()

    def tearDown(self):
        pass

    def test_return_latest_strip(self):
        testdata1 = open(TESTDATA_FILENAME.format("1")).read()
        
        # Test cornercases
        result = self._gear._get_strip_for_date("", arrow.get("2020-01-14"), True)
        self.assertIsNone(result)
        result = self._gear._get_strip_for_date(testdata1, arrow.get("2020-01-20"), True)
        self.assertIsNone(result)
        result = self._gear._get_strip_for_date(testdata1, arrow.get("2020-01-20"), False)
        self.assertEqual("No new CommitStrip for today", result)

        # Real test
        result = self._gear._get_strip_for_date(testdata1, arrow.get("2020-01-14"), True)
        self.assertEqual("New CommitStrip content: {}\n{}".format(
                "Other people’s code",
                "https://www.commitstrip.com/wp-content/uploads/2020/01/Strip-Paywall-650-finalenglish.jpg"
            ), result)

