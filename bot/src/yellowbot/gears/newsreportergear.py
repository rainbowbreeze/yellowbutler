"""A YellowBot gear to check for news from different sources, and send them over a surface.

This class controls various source of information, like RSS feeds, YouTube
 channels, misc pages, etc, and checks if there are updated content since the
 last check.
Once updates are found, they're send over a surface to notify the user.

Requirements
- requests
- arrow
"""

from logging import Logger
import requests
from arrow import Arrow
import arrow

from types import SimpleNamespace
from typing import Any, Dict, List, Optional, TypeVar, Union

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
        newssources_urls: list,
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
        self._newssources_urls = newssources_urls
        self._storage = storage_service

    def process_intent(
        self,
        intent: str,
        params: Dict[str, Any]
    ) -> Optional[str]:

        if NewsReportGear.INTENTS[0] != intent:
            message = "Call to {} using wrong intent {}".format(__name__, intent)
            self._logger.info(message)
            return message 

        # Defaul value for silent param
        silent = False
        if NewsReportGear.PARAM_SILENT in params:
            silent = params[NewsReportGear.PARAM_SILENT]

        self._logger.info("Start processing new news to report")
        return self._find_daily_news(silent)

    def _find_daily_news(self, silent: bool) -> Optional[str]:
        """Analyze all the different news sources, notifying in case new contents are found

        :param silent: if True, doesn't produce any value when new content is not found
        :type silent: bool

        :returns: a message with the result of the processing
        :rtype: str
        """

        # use when last check date is not available for a news source
        #  Default is 5 days in the past
        fallback_check_date: Arrow = arrow.utcnow().shift(days=-6) 

        messages = []
        for newssource_url in self._newssources_urls:
            self._logger.info("Checking for news on {}".format(newssource_url))

            #TODO distinguish between different news sources
            messages.extend(self._analize_youtube_channel(newssource_url, fallback_check_date))

        if 0 == len(messages) and not silent:
            message = "No new news for today"
        else:
            message = "\n".join(messages)
        
        return message

    def _analize_youtube_channel(
        self,
        channel_url: str,
        fallback_check_date: Arrow
    ) -> List[str]:
        """Analyze a YouTube channel searching for new videos

        :param channel_url: the full url of the Youtube channel to analyze. E.g.: https://www.youtube.com/channel/UCSbdMXOI_3HGiFviLZO6kNA
        :type channel_url: str

        :param fallback_check_date: date to use for checking, in case no previous check was performed on the news source
        :type fallback_check_date: Arrow

        :returns: a list of str, each one containing a new content (video) found on the channel. It could also potentially contains an error message
        :rtype: list[str]
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
        news_items = None
        self._logger.debug("Reading from the db entity for channel_url {}".format(channel_url))
        try:
            news_items = self._storage.get_by_property(NewsItemEntity, "url", "=", channel_url)
        except BaseException as err:
            self._logger.exception("Error while reading the entity from the storage: {}".format(err))

        if news_items is None or 0 == len(news_items):
            # Creates the item
            self._logger.info("This is the first time the source {} is processed for updates".format(channel_url))
            news_item = NewsItemEntity()
            news_item.url = channel_url
        else:
            news_item = news_items[0]

        video_update_messages: List[str] = []  # Initialize the return var

        # param1 may have the special upload playlist id. otherwise obtain it from a YouTube API call
        upload_playlist_id = None
        if hasattr(news_item, "param1") and news_item.param1:
            upload_playlist_id = news_item.param1
            self._logger.debug("Using stored playlist ID {}".format(upload_playlist_id))
        else:
            channel_id = self._youtube_extract_channel_id_from_url(channel_url)
            # Find the upload playlist id for the given channel
            try:
                upload_playlist_id = self._youtube_find_upload_playlist_from_channel(self._youtube_api_key, channel_id)
            except BaseException as err:
                # Forge specific messagge to return to the caller
                video_update_messages.append("Error getting information on YouTube channel {}".format(channel_id))
                return video_update_messages
            news_item.param1 = upload_playlist_id
        
        # Search latest videos in the upload playlist
        try:
            all_videos = self._youtube_find_new_videos_in_a_playlist(self._youtube_api_key, upload_playlist_id)
        except BaseException as err:
                # Forge specific messagge to return to the caller
                video_update_messages.append("Error getting information on playlist {} for channel {}".format(
                    upload_playlist_id,
                    channel_url)
                )
                return video_update_messages

        # Find in the db the last check date
        if hasattr(news_item, "last_check"):
            self._logger.debug("Found last_check in the stored entity: {}".format(news_item.last_check))
            last_check_date: Arrow = arrow.get(news_item.last_check)
        else:
            self._logger.debug("Stored entity has no last_check property")
            last_check_date = fallback_check_date

        self._logger.debug("Comparing published date of {} videos agains {}".format(
            len(all_videos),
            last_check_date
        ))

        # Discard all the videos older that a certain date
        newer_videos = []
        for video in all_videos:
            # Get date from the video
            published_date = arrow.get(video.published)
            if published_date > last_check_date:
                newer_videos.append(video)
        self._logger.info("Found {} videos, out of {}, newer than {}".format(
            len(newer_videos),
            len(all_videos),
            last_check_date
        ))

        # Store the values
        try:
            # Convert Arrow object back to datetime
            news_item.last_check = arrow.utcnow().datetime
            self._logger.debug("Updating the news entity with new date {}".format(news_item.last_check))
            self._storage.put(news_item)
        except BaseException as err:
            self._logger.exception("Error while saving the entity to the storage: {}".format(err))

        # Create alerts for the new videos
        for video in newer_videos:
            message = 'New video published: {} - {}'.format(
                video.title,
                video.url
            )
            video_update_messages.append(message)

        return video_update_messages


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

        :raises: BaseException if there are some errors in using the Youtube API

        :param api_key: the API key to use for YouTube API v3 calls
        :type api_key: str

        :param channel_id: the id of the channel where the search is performed
        :type channel_id: str

        :returns: the id of the special "upload" playlist
        :rtype: str

        """

        self._logger.info("Retrieving YouTube channel information for {}".format(channel_id))
        url = 'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&id={}&key={}'.format(
            channel_id,
            api_key
        )

        try:
            req = requests.get(url)
            if not req.ok:
                req.raise_for_status()
            results = req.json()
            self._logger.debug("Data read from channel: {}".format(results))
        except BaseException as err:
            self._logger.exception("Error while getting information for channel {}: {}".format(
                channel_id,
                err
            ))
            raise err

        try:
            channel_items = results['items']
            upload_id = channel_items[0]['contentDetails']['relatedPlaylists']['uploads']
        except BaseException as err:
            self._logger.exception("Exception happened while parsing YouTube data {}".format(err))
            raise err

        return upload_id

    def _youtube_find_new_videos_in_a_playlist(
        self,
        api_key: str,
        playlist_id: str
    ) -> List[SimpleNamespace]:
        """Given a playlist, it searched for its latest videos

        :raises: BaseException if there are some errors in using the Youtube API

        :param api_key: the API key to use for YouTube API v3 calls
        :type api_key: str

        :param playlist_id: the id of the playlist
        :type playlist_id: str

        :returns: a collection of objects, representing videos
        :rtype: list
        """

        self._logger.debug("Retrieving playlist information for {}".format(playlist_id))
        url = 'https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=5&playlistId={}&key={}'.format(
            playlist_id,
            api_key
        )

        try:
            req = requests.get(url)
            if not req.ok:
                req.raise_for_status()
            results = req.json()
            self._logger.debug("Data read from playlist: {}".format(results))
        except BaseException as err:
            self._logger.exception("Error while getting playlist information for playlist {}: {}".format(
                playlist_id,
                err
            ))
            raise err

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
        except BaseException as err:
            self._logger.exception("Exception happened while parsing data for playlist {}: {}".format(
                playlist_id,
                err
            ))
            raise err

        self._logger.debug("{} videos found on the playlist {}".format(
            len(latest_videos),
            playlist_id
        ))
        return latest_videos
