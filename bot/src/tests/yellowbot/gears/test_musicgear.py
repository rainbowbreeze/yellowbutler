"""
Test for Music gear
"""
from unittest import TestCase

from yellowbot.gears.musicgear import MusicGear
from yellowbot.globalbag import GlobalBag


class TestMusicGear(TestCase):
    def setUp(self):
        self._gear = MusicGear("test_url", True)
        pass

    def tearDown(self):
        pass

    def test_process_intent(self):
        result = self._gear.process_intent(
            GlobalBag.TRACE_MUSIC_INTENT,
            {
                GlobalBag.TRACE_MUSIC_PARAM_AUTHOR: "Author1",
                GlobalBag.TRACE_MUSIC_PARAM_TITLE: "Title1"
            }
        )

        assert "Title1 by Author1 has been added" == result
