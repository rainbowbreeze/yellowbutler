"""
Test for the NLU engine
"""
from unittest import TestCase

from yellowbot.gears.musicgear import MusicGear
from yellowbot.globalbag import GlobalBag


class TestMusicGear(TestCase):
    def setUp(self):
        self._gear = MusicGear()
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

        assert "Sorry, I still don't know how to keep track of Title1 by Author1" == result
