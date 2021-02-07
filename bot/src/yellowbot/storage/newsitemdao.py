"""Data Access Object to manage NewsItem.

It could use different types of storage service, and the one to use is injected
 during the class initialization


"""

from yellowbot.storage.basestorageservice import BaseStorageService
from yellowbot.storage.newsitementity import NewsItemEntity

class NewsItemDao:

    def __init__(self, storage_service: BaseStorageService):
        """Initialize the class

        :param storage_service: the storage service to use
        :type storage_service: DataStorageService
        """

        self._storage_service = storage_service

    def get_newsitem(self, url: str) -> NewsItemEntity:
        """Search for a news item on the storage, given its url

        :param url: the url of the news item
        :type url: str

        :returns: the NewsItem searched, otherwise null
        :rtype: NewsItemEntity
        """

        self._storage_service.query()
        return None

    def save_newsitem(self, newsitem: NewsItemEntity) -> NewsItemEntity:
        """Save a news item into the storage

        :param newsitem: the news item to save
        :type newsitem: NewsItemEntity

        :returns: the newsitem saved
        :rtype: NewsItemEntity
        """

        self._storage_service.put(newsitem)
        return newsitem



