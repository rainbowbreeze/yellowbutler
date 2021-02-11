"""Test CommitStrip gear

Responses library is used to mock Request calls
https://github.com/getsentry/responses

Unfortunately, PyTest fixtures feature do not work when pytest is used in unittest.TestCase subclasses, apart from Auto-use fixtures.
Source: https://docs.pytest.org/en/stable/unittest.html#pytest-features-in-unittest-testcase-subclasses
"""
from unittest import TestCase
import responses
import os
import arrow

from yellowbot.gears.commitstripgear import CommitStripGear
from yellowbot.globalbag import GlobalBag

TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), "testdata_commitstrip_{}.txt")


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
    
    @responses.activate
    def test_mock_request(self):
        testdata1 = open(TESTDATA_FILENAME.format("1")).read()

        # Use responses to provide a predefined value when the testes class calls requests
        responses.add(
            responses.GET,
            'http://www.commitstrip.com/en/feed/',
            body = testdata1,
            status = 200,
            content_type='application/xml'
        )

        result = self._gear._find_daily_strip(False)
        self.assertEqual("No new CommitStrip for today", result)
        # Unfortunately, I don't have parameters to pass a specific day at this level.
        #  But, at least, I verified the responses mechanism works

    @responses.activate
    def test_simulate_error_in_request(self):
        # This test also checks that responses are not carried over from one
        #  test to another, and each test starts the responses routes empty 

        responses.add(
            responses.GET,
            'http://www.commitstrip.com/en/feed/',
            body = '',
            status = 404,
            content_type='application/xml'
        )

        result = self._gear._find_daily_strip(False)
        self.assertEqual('Error while reading RSS feed from CommitStrip: 404 Client Error: Not Found for url: http://www.commitstrip.com/en/feed/', result)
