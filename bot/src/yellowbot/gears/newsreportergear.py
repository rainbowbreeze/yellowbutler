"""
A YellowBot gear to check for news from different sources, and send them over
 a surface

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
    """
    Check updates from different sources and send them to a specific surface

    """
    INTENTS = [GlobalBag.CHECKFORNEWS_INTENT]
    # PARAM_SILENT = GlobalBag.COMMITSTRIP_PARAM_SILENT  # No notification if there is nothing new 

    def __init__(self,
                 test_mode = False):
        """
        """
        BaseGear.__init__(self, NewsReportGear.__name__, self.INTENTS)
        self._logger = LoggingService.get_logger(__name__)
        self._test_mode = test_mode

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
        """
        Analyze all the different news sources, notifying in case new contents
         are found
        """

        # Based on the source address, it calls a different logic
        return
    
    def _analize_youtube_channel(self, youtube_channel_id):
        """
        Analyze a YouTube channel searching for new videos

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

        # Find the upload playlist id for the given channel

        # Search latest videos in the upload playlist

        channel_id = 'UCSbdMXOI_3HGiFviLZO6kNA'
        upload_id = 'UUSbdMXOI_3HGiFviLZO6kNA' # Slightly different
        api_key = 'AIzaSyD0es8hfz0z85ZAP5CM5k6o9pLtX6SgpyI'

        url = 'https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=2&playlistId={}&key={}'.format(
            upload_id,
            api_key
        )

        try:
            req = requests.get(url)
            if not req.ok:
                req.raise_for_status()
            results = req.json()
        except BaseException as e:
            self._logger.exception(e)
            return "Error while getting playlist information for channel {} and playlist {}: {}".format(
                channel_id,
                upload_id,
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


