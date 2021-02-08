"""A YellowBot gear to check for news from different sources, and send them over a surface.

This class controls various source of information, like RSS feeds, YouTube
 channels, misc pages, etc, and checks if there are updated content since the
 last check.
Once updates are found, they're send over a surface to notify the user.

Requirements
- requests
- arrow
"""

import requests
import arrow

from types import SimpleNamespace
from typing import List, Optional, TypeVar, Union
from distutils.util import strtobool
import datetime

from yellowbot.gears.basegear import BaseGear
from yellowbot.globalbag import GlobalBag
from yellowbot.loggingservice import LoggingService
from yellowbot.storage.basestorageservice import BaseStorageService
from yellowbot.storage.newsitementity import NewsItemEntity

BSS = TypeVar('BSS', bound=BaseStorageService)
# See here for explanation: https://www.python.org/dev/peps/pep-0484/#the-type-of-class-objects

class NewsReportGear(BaseGear):
    """Check updates from different sources and send them to a specific surface
    """

    INTENTS = [GlobalBag.CHECKFORNEWS_INTENT]
    PARAM_SILENT = GlobalBag.CHECKFORNEWS_PARAM_SILENT  # No notification if there is nothing new 

    def __init__(
        self,
        youtube_api_key: str,
        storage_service: BSS
    ) -> None:
        """Constructor

        :param youtube_api_key: the API key to use for YouTube API v3 calls
        :type api_key: str 

        :param storage_service: the storage service to use. Caller object will decide the specific implementation
        :type storaga_service: BaseStorageService subclass
        """

        super().__init__(self.__class__.__name__, self.INTENTS)
        self._logger = LoggingService.get_logger(__name__)
        self._youtube_api_key = youtube_api_key
        self._storage = storage_service

    def process_intent(
        self,
        intent: str,
        params: List[str]
    ) -> Union[Optional[str], List[str]]:
        if NewsReportGear.INTENTS[0] != intent:
            message = "Call to {} using wrong intent {}".format(__name__, intent)
            self._logger.info(message)
            return message 

        # Defaul value for silent param
        silent = False
        if NewsReportGear.PARAM_SILENT in params:
            # https://stackoverflow.com/a/35412300
            silent = bool(strtobool(params[NewsReportGear.PARAM_SILENT]))

        return self._find_daily_news(silent)

    def _find_daily_news(self, silent: bool) -> Union[Optional[str], List[str]]:
        """Analyze all the different news sources, notifying in case new contents are found

        :param silent: if True, doesn't produce any value when new content is not found
        :type silent: bool

        :returns: a message with the result of the processing
        :rtype: str
        """

        channel_urls = [
            'https://www.youtube.com/channel/UCSbdMXOI_3HGiFviLZO6kNA'
        ]
        today = arrow.utcnow()

        message = None
        for channel_url in channel_urls:
            self._logger.info("Checking for news on {}".format(channel_url))
            #TODO check for errors
            videos = self._analize_youtube_channel(channel_url, datetime.datetime.now())
            #TODO check for errors
            for video in videos:
                self._logger.info("Found new video {}".format(video.url))
                # Good, the video was published today
                message = 'New video published: {}\n{}'.format(
                    video.title,
                    video.url
                )
                break
        
        if not message and not silent:
            message = "No new videos for today"
        
        return message

    def _analize_youtube_channel(
        self,
        channel_url: str,
        last_check: datetime.date
    ) -> List[SimpleNamespace]:
        """Analyze a YouTube channel searching for new videos

        :param channel_url: the full url of the Youtube channel to analyze. E.g.: https://www.youtube.com/channel/UCSbdMXOI_3HGiFviLZO6kNA
        :type channel_url: str

        :param last_check_date: last check date for the videos
        :type channel_url: datetime.date

        :returns: TDB, the list of the latest channel videos
        :rtype: list
        """

        # Every channel as a special playlist called upload, with all the 
        #  latest uploaded videos in the channel. Checking for videos
        #  in this playlist has a YouTube API quota cost of 1, while
        #  performing a normal search on all the new videos for a channel has
        #  a quota cost of 100.
        # So, it's wortwhile to first check for the upload playlist id for
        #  the channel, cache it, and then search for new videos inside
        #  this playlist

        # Search in the database if it has already information for the given
        #  channel, included the playlist id 
        try:
            news_items = self._storage.get_by_property(NewsItemEntity, "url", "=", channel_url)
        except BaseException as e:
            self._logger.error(e)
            news_items = None

        if news_items is None or 0 == len(news_items):
            # Creates the item
            news_item = NewsItemEntity()
            news_item.url = channel_url
        else:
            news_item = news_items[0]

        # Retrieve the key from the DB. otherwise obtain it from a YouTube API call
        if hasattr(news_items, "param1") and news_item.param1:
            upload_playlist_id = news_item.param1
        else:
            channel_id = self._youtube_extract_channel_id_from_url(channel_url)
            # Find the upload playlist id for the given channel
            upload_playlist_id = self._youtube_find_upload_playlist_from_channel(self._youtube_api_key, channel_id)
            #TODO error management
            news_item.param1 = upload_playlist_id

        # Search latest videos in the upload playlist
        all_videos = self._youtube_find_new_videos_in_a_playlist(self._youtube_api_key, upload_playlist_id)

        # Find in the db the last check date
        #TODO last_check is from the NewsItemEntity, not passed as parameter

        # Discard all the videos older that a certain date
        post_check_videos = []
        for video in all_videos:
            if self._published_post_check(last_check, video.published):
                post_check_videos.append(video)

        # Store the values
        try:
            news_item.last_check = last_check
            self._storage.put(news_item)
        except BaseException as e:
            self._logger.error(e)

        # Send alerts for the next videos
        return post_check_videos


    def _youtube_extract_channel_id_from_url(self, channel_url: str) -> str:
        """Extract the channel id from the channel URL

        For https://www.youtube.com/channel/UCSbdMXOI_3HGiFviLZO6kNA, it returns UCSbdMXOI_3HGiFviLZO6kNA

        :param channel_url: YouTube channel url
        :type channel_url: str

        :returns: channel id only
        :rtype: str
        """

        # More elegant regex solution: https://stackoverflow.com/questions/51166723/extract-youtube-channel-id-from-channel-url-android
        return channel_url[len('https://www.youtube.com/channel/'):]

    def _youtube_find_upload_playlist_from_channel(
        self,
        api_key: str,
        channel_id: str
    ) -> str:
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


    def _youtube_find_new_videos_in_a_playlist(
        self,
        api_key: str,
        playlist_id: str
    ) -> List[SimpleNamespace]:
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
            self._logger.error("Error while getting playlist information for playlist {}: {}".format(
                playlist_id,
                repr(e)
            ))
            self._logger.exception(e)
            raise e

        latest_videos = []
        try:
            for item in results['items']:
                snippet = item['snippet']
                video_url = 'https://www.youtube.com/watch?v={}'.format(
                    snippet['resourceId']['videoId'])
                video_title = snippet['title']
                video_published = snippet['publishedAt']

                # Power of SimpleNamespace class
                video = SimpleNamespace(
                    url = video_url,
                    title = video_title,
                    published = video_published
                )
                latest_videos.append(video)
        except BaseException as e:
            self._logger.error("Exception happened while parsing YouTube data {}".format(repr(e)))
            self._logger.exception(e)
            raise e

        return latest_videos

    def _published_post_check(
        self,
        last_check: datetime.date,
        video_published: datetime.date
    ) -> bool:
        """Check if a given content was published after a certain data
        """
        last_check_date = arrow.get(last_check)
        video_publish_date = arrow.get(video_published)

        last_check_date = arrow.utcnow()
        return last_check_date.format("YYYY-MM-DD") == video_publish_date.format("YYYY-MM-DD")
