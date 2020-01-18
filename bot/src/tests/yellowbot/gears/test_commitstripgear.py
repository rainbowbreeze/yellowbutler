"""
Test CommitStrip gear
"""
from unittest import TestCase

import os

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
        result = self._gear._return_latest_strip("")
        self.assertIsNone(result)

        result = self._gear._return_latest_strip(testdata1)
        self.assertEqual("Tue, 14 Jan 2020 20:03:56 +0000", result)
