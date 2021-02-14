"""Test NewsReportGear

Responses library is used to mock Request calls
https://github.com/getsentry/responses
"""

from unittest import TestCase
import responses
import os
import arrow
import pytest

from yellowbot.gears.newsreportergear import NewsReportGear
from yellowbot.globalbag import GlobalBag
from yellowbot.storage.basestorageservice import BaseStorageService
from yellowbot.storage.newsitementity import NewsItemEntity

# https://docs.pytest.org/en/stable/warnings.html#deprecationwarning-and-pendingdeprecationwarning
@pytest.mark.filterwarnings("ignore:To avoid breaking existing software while fixing issue 310.*:DeprecationWarning")
class TestNewsReportGear(TestCase):
    TESTDATA_YOUTUBE_CHANNEL_FILENAME = os.path.join(os.path.dirname(__file__), "testdata_youtube_channel.txt")
    TESTDATA_YOUTUBE_PLAYLIST_FILENAME = os.path.join(os.path.dirname(__file__), "testdata_youtube_playlist.txt")
    TESTDATA_RSS_FEED_1_FILENAME = os.path.join(os.path.dirname(__file__), "testdata_rssfeed_1.txt")
    TESTDATA_ATOM_1_FILENAME = os.path.join(os.path.dirname(__file__), "testdata_atom_1.txt")

    def setUp(self):
        self._youtube_key = 'mock_youtube_key'
        self._gear = NewsReportGear(self._youtube_key, [], BaseStorageService())

    def tearDown(self):
        pass

    def test_youtube_extract_channel_id_from_url(self):
        self.assertEqual('UCSbdMXOI_3HGiFviLZO6kNA', self._gear._youtube_extract_channel_id_from_url('https://www.youtube.com/channel/UCSbdMXOI_3HGiFviLZO6kNA'))
        self.assertEqual('UCkRfArvrzheW2E7b6SVT7vQ', self._gear._youtube_extract_channel_id_from_url('https://www.youtube.com/channel/UCkRfArvrzheW2E7b6SVT7vQ'))


    @responses.activate
    def test_youtube_find_upload_playlist_from_channel(self):
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

    @responses.activate
    def test_youtube_analize_channel(self):
        testdata1 = open(self.TESTDATA_YOUTUBE_CHANNEL_FILENAME).read()
        testdata2 = open(self.TESTDATA_YOUTUBE_PLAYLIST_FILENAME).read()
        responses.add(
            responses.GET,
            'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&id=UCSbdMXOI_3HGiFviLZO6kNA&key=mock_youtube_key',
            body = testdata1,
            status = 200,
            content_type='application/json'
        )
        responses.add(
            responses.GET,
            'https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=5&playlistId=UUSbdMXOI_3HGiFviLZO6kNA&key=mock_youtube_key',
            body = testdata2,
            status = 200,
            content_type='application/json'
        )

        news_item = NewsItemEntity()
        news_item.url = "https://www.youtube.com/channel/UCSbdMXOI_3HGiFviLZO6kNA"
        new_videos = self._gear._youtube_analize_channel(
            news_item,
            arrow.utcnow()
        )
        # There are no videos for current data, as all the mock data refers to past vides
        self.assertEqual(0, len(new_videos))

        new_videos = self._gear._youtube_analize_channel(
            news_item,
            arrow.get("2021-02-02T00:15:04Z")
        )
        self.assertEqual(1, len(new_videos))
        self.assertEqual("New video published: The 7 Types of VR Users 2 - https://www.youtube.com/watch?v=WFeny7l1Ev4", new_videos[0])

        new_videos = self._gear._youtube_analize_channel(
            news_item,
            arrow.get("2021-01-26T10:00:10Z")
        )
        self.assertEqual(2, len(new_videos))
        self.assertEqual("New video published: The 7 Types of VR Users 2 - https://www.youtube.com/watch?v=WFeny7l1Ev4", new_videos[0])
        self.assertEqual("New video published: Valve's next VR projects are SCARILY similar to Sword Art Online - https://www.youtube.com/watch?v=veVx0AuhHFw", new_videos[1])

    @responses.activate
    def test_rss_analize_channel_rss_feed(self):
        testdata1 = open(self.TESTDATA_RSS_FEED_1_FILENAME).read()
        responses.add(
            responses.GET,
            "https://developer.oculus.com/blog/rss/",
            body = testdata1,
            status = 200,
            content_type='application/xml'
        )

        new_feeds = self._gear._rss_analize_channel(
            "https://developer.oculus.com/blog/rss/",
            arrow.utcnow()
        )
        # There are no videos for current data, as all the mock data refers to past vides
        self.assertEqual(0, len(new_feeds))

        new_feeds = self._gear._rss_analize_channel(
            "https://developer.oculus.com/blog/rss/",
            arrow.get("2021-02-01T08:00:10Z")
        )
        self.assertEqual(1, len(new_feeds))
        self.assertEqual("New article published: Introducing App Lab: A New Way to Distribute Oculus Quest Apps - https://developer.oculus.com/blog/introducing-app-lab-a-new-way-to-distribute-oculus-quest-apps/", new_feeds[0])

        new_feeds = self._gear._rss_analize_channel(
            "https://developer.oculus.com/blog/rss/",
            arrow.get("2021-01-20T08:00:10Z")
        )
        self.assertEqual(4, len(new_feeds))
        self.assertEqual("New article published: Introducing App Lab: A New Way to Distribute Oculus Quest Apps - https://developer.oculus.com/blog/introducing-app-lab-a-new-way-to-distribute-oculus-quest-apps/", new_feeds[0])
        self.assertEqual("New article published: Art Direction for All-in-One VR Performance - https://developer.oculus.com/blog/art-direction-for-all-in-one-vr-performance/", new_feeds[1])
        self.assertEqual("New article published: Verify Your Oculus Developer Account by February 1 - https://developer.oculus.com/blog/verify-your-oculus-developer-account-by-february-1/", new_feeds[2])
        self.assertEqual("New article published: Now Available: VR Locomotion Design Guide - https://developer.oculus.com/blog/now-available-vr-locomotion-design-guide/", new_feeds[3])

    @responses.activate
    def test_rss_analize_channel_atom_feed(self):
        testdata1 = open(self.TESTDATA_ATOM_1_FILENAME).read()
        responses.add(
            responses.GET,
            "https://www.home-assistant.io/atom.xml",
            body = testdata1,
            status = 200,
            content_type='application/xml'
        )

        new_feeds = self._gear._rss_analize_channel(
            "https://www.home-assistant.io/atom.xml",
            arrow.utcnow()
        )
        # There are items for current data, as all the mock data refers to past vides
        self.assertEqual(0, len(new_feeds))

        new_feeds = self._gear._rss_analize_channel(
            "https://www.home-assistant.io/atom.xml",
            arrow.get("2021-02-11T00:00:00+00:00")
        )
        self.assertEqual(1, len(new_feeds))
        self.assertEqual("New article published: Community Highlights: 8th edition - https://www.home-assistant.io/blog/2021/02/12/community-highlights/", new_feeds[0])

        new_feeds = self._gear._rss_analize_channel(
            "https://www.home-assistant.io/atom.xml",
            arrow.get("2021-02-02T00:00:00+00:00")
        )
        self.assertEqual(2, len(new_feeds))
        self.assertEqual("New article published: Community Highlights: 8th edition - https://www.home-assistant.io/blog/2021/02/12/community-highlights/", new_feeds[0])
        self.assertEqual("New article published: 2021.2: Z-Wave... JS! - https://www.home-assistant.io/blog/2021/02/03/release-20212/", new_feeds[1])

        new_feeds = self._gear._rss_analize_channel(
            "https://www.home-assistant.io/atom.xml",
            arrow.get("2021-01-22T00:00:00+00:00")
        )
        self.assertEqual(4, len(new_feeds))
        self.assertEqual("New article published: Community Highlights: 8th edition - https://www.home-assistant.io/blog/2021/02/12/community-highlights/", new_feeds[0])
        self.assertEqual("New article published: 2021.2: Z-Wave... JS! - https://www.home-assistant.io/blog/2021/02/03/release-20212/", new_feeds[1])
        self.assertEqual("New article published: Security Disclosure 2: vulnerabilities in custom integrations HACS, Font Awesome and others - https://www.home-assistant.io/blog/2021/01/23/security-disclosure2/", new_feeds[2])
        self.assertEqual("New article published: Disclosure: security vulnerabilities in custom integrations HACS, Dwains Dashboard, Font Awesome and others - https://www.home-assistant.io/blog/2021/01/22/security-disclosure/", new_feeds[3])

