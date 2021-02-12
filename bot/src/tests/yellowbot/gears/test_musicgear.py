"""
Test for Music gear
"""
from unittest import TestCase

from yellowbot.gears.musicgear import MusicGear
from yellowbot.globalbag import GlobalBag


class TestMusicGear(TestCase):
    def setUp(self):
        self._gear = MusicGear("test_url", True)

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

        self.assertIsNotNone(result)
        self.assertTrue(result.went_well())
        self.assertTrue(result.has_messages())
        messages = result.get_messages()
        self.assertEqual(1, len(messages))
        self.assertEqual("Title1 by Author1 has been added", messages[0])
