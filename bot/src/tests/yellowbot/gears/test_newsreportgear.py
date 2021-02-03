"""Test NewsReportGear

Responses library is used to mock Request calls
https://github.com/getsentry/responses
"""

from unittest import TestCase
import responses
import os
import arrow

from yellowbot.gears.newsreportergear import NewsReportGear
from yellowbot.globalbag import GlobalBag

class TestNewsReportGear(TestCase):
    TESTDATA_YOUTUBE_CHANNEL_FILENAME = os.path.join(os.path.dirname(__file__), "testdata_youtube_channel.txt")
    TESTDATA_YOUTUBE_PLAYLIST_FILENAME = os.path.join(os.path.dirname(__file__), "testdata_youtube_playlist.txt")

    def setUp(self):
        self._youtube_key = 'mock_youtube_key'
        self._gear = NewsReportGear(self._youtube_key)

    def tearDown(self):
        pass

    @responses.activate
    def test_youtube_upload_playlist_from_channel(self):
        testdata = open(self.TESTDATA_YOUTUBE_CHANNEL_FILENAME).read()

        # For channel_id = 'UCSbdMXOI_3HGiFviLZO6kNA'
        # expected upload_playlist_id = 'UUSbdMXOI_3HGiFviLZO6kNA' # Slightly different

        responses.add(
            responses.GET,
            'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&id=UCSbdMXOI_3HGiFviLZO6kNA&key=mock_youtube_key',
            body = testdata,
            status = 200,
            content_type='application/json'
        )

        result = self._gear._youtube_find_upload_playlist_from_channel(self._youtube_key, 'UCSbdMXOI_3HGiFviLZO6kNA')
        self.assertEqual('UUSbdMXOI_3HGiFviLZO6kNA', result)
    
    @responses.activate
    def test_youtube_find_new_videos_in_a_playlist(self):
        testdata = open(self.TESTDATA_YOUTUBE_PLAYLIST_FILENAME).read()

        responses.add(
            responses.GET,
            'https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=5&playlistId=UUSbdMXOI_3HGiFviLZO6kNA&key=mock_youtube_key',
            body = testdata,
            status = 200,
            content_type='application/json'
        )

        results = self._gear._youtube_find_new_videos_in_a_playlist(self._youtube_key, 'UUSbdMXOI_3HGiFviLZO6kNA')
        self.assertEqual(10, len(results))

        item = results[0]
        self.assertEqual('https://www.youtube.com/watch?v=WFeny7l1Ev4', item.url)
        self.assertEqual('The 7 Types of VR Users 2', item.title)
        self.assertEqual('2021-02-02T19:15:04Z', item.published)

        item = results[1]
        self.assertEqual('https://www.youtube.com/watch?v=veVx0AuhHFw', item.url)
        self.assertEqual('Valve\'s next VR projects are SCARILY similar to Sword Art Online', item.title)
        self.assertEqual('2021-01-27T20:00:10Z', item.published)

        item = results[2]
        self.assertEqual('https://www.youtube.com/watch?v=lILlWMLTn0c', item.url)
        self.assertEqual('What Happened to my Valve Index After 2000 Hours?', item.title)
        self.assertEqual('2021-01-23T19:15:01Z', item.published)

        item = results[3]
        self.assertEqual('https://www.youtube.com/watch?v=EzHjucDrNsY', item.url)
        self.assertEqual('The Oculus Quest 2 gets a HUGE Update for QoL', item.title)
        self.assertEqual('2021-01-19T19:35:57Z', item.published)

        item = results[4]
        self.assertEqual('https://www.youtube.com/watch?v=PIIXyfuxOcU', item.url)
        self.assertEqual('CES 2021 brings INSANE new VR Technology', item.title)
        self.assertEqual('2021-01-12T19:13:35Z', item.published)
