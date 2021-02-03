"""A YellowBot gear to check for news from different sources, and send them over a surface.

This class controls various source of information, like RSS feeds, YouTube
 channels, misc pages, etc, and checks if there are updated content since the
 last check.
Once updates are found, they're send over a surface to notify the user.

Requirements
- requests
- feedparser
- arrow
"""

import requests

from types import SimpleNamespace

from yellowbot.gears.basegear import BaseGear
from yellowbot.globalbag import GlobalBag
from yellowbot.loggingservice import LoggingService

class NewsReportGear(BaseGear):
    """Check updates from different sources and send them to a specific surface
    """

    INTENTS = [GlobalBag.CHECKFORNEWS_INTENT]
    # PARAM_SILENT = GlobalBag.COMMITSTRIP_PARAM_SILENT  # No notification if there is nothing new 

    def __init__(self,
                 youtube_api_key,
                 test_mode = False):
        """Constructor

        :param youtube_api_key: the API key to use for YouTube API v3 calls
        :type api_key: str 
        """

        BaseGear.__init__(self, NewsReportGear.__name__, self.INTENTS)
        self._logger = LoggingService.get_logger(__name__)
        self._test_mode = test_mode
        self._youtube_api_key = youtube_api_key

    def process_intent(self, intent, params):
        if NewsReportGear.INTENTS[0] != intent:
            message = "Call to {} using wrong intent {}".format(__name__, intent)
            self._logger.info(message)
            return message 

        # Defaul value for silent param
        #silent = False
        #if CommitStripGear.PARAM_SILENT in params:
        #    silent = params[CommitStripGear.PARAM_SILENT]

        return self._analize_youtube_channel('')

    def _analyze_and_notify_news_sources(self):
        """Analyze all the different news sources, notifying in case new
         contents are found
        """

        # Based on the source address, it calls a different logic
        return
    
    def _analize_youtube_channel(self, youtube_channel_id):
        """Analyze a YouTube channel searching for new videos

        :param youtube_channel_id: the id of the channel to analyze
        :type youtube_channel_id: str
        """

        # Every channel as a special playlist called upload, with all the 
        #  latest uploaded videos in the channel. Checking for videos
        #  in this playlist has a YouTube API quota cost of 1, while
        #  performing a normal search on all the new videos of a channel has
        #  a quota cost of 100.
        # So, it's wortwhile to first check for the upload playlist id for
        #  the channel, cache it, and then search for new videos inside
        #  this playlist

        # Search in the database if it has already the "upload" playlist id 
        #  for the given channel.
        # This pla
        upload_playlist_id = self._youtube_find_upload_playlist_from_channel(self._youtube_api_key, youtube_channel_id)
        self._youtube_find_new_videos_in_a_playlist(self._youtube_api_key, upload_playlist_id)

        # Find the upload playlist id for the given channel

        # Search latest videos in the upload playlist

    def _youtube_find_upload_playlist_from_channel(self, api_key, channel_id):
        """Find upload playlist id for a given channel

        :param api_key: the API key to use for YouTube API v3 calls
        :type api_key: str

        :param channel_id: the id of the channel where the search is performed
        :type channel_id: str

        :returns: the id of the special "upload" playlist
        :rtype: str
        """

        url = 'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&id={}&key={}'.format(
            channel_id,
            api_key
        )

        try:
            req = requests.get(url)
            if not req.ok:
                req.raise_for_status()
            results = req.json()
        except BaseException as e:
            self._logger.exception(e)
            return "Error while getting information for channel {}: {}".format(
                channel_id,
                repr(e)
            )

        upload_id = None
        try:
            channel_items = results['items']
            upload_id = channel_items[0]['contentDetails']['relatedPlaylists']['uploads']
        except BaseException as e:
            return "Exception happened while parsing YouTube data {}".format(repr(e))        

        return upload_id


    def _youtube_find_new_videos_in_a_playlist(self, api_key, playlist_id):
        """Given a playlist, it searched for its latest videos

        :param api_key: the API key to use for YouTube API v3 calls
        :type api_key: str

        :param playlist_id: the id of the playlist
        :type playlist_id: str

        :returns: a collection of objects, representing videos
        :rtype: list
        """

        url = 'https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=5&playlistId={}&key={}'.format(
            playlist_id,
            api_key
        )

        try:
            req = requests.get(url)
            if not req.ok:
                req.raise_for_status()
            results = req.json()
        except BaseException as e:
            self._logger.exception(e)
            return "Error while getting playlist information for playlist {}: {}".format(
                playlist_id,
                repr(e)
            )

        latest_videos = []
        try:
            for item in results['items']:
                snippet = item['snippet']
                video_url = 'https://www.youtube.com/watch?v={}'.format(
                    snippet['resourceId']['videoId'])
                video_title = snippet['title']
                video_published = snippet['publishedAt']

                video = SimpleNamespace(
                    url = video_url,
                    title = video_title,
                    published = video_published
                )
                latest_videos.append(video)
        except BaseException as e:
            return "Exception happened while parsing YouTube data {}".format(repr(e))        

        return latest_videos





