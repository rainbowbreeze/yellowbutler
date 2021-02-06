"""Implement a storage service based on the filesystem

Currently it uses TinyDB, but it's transparent (more or less) to the outside world
 https://pypi.python.org/pypi/tinydb/

Examples
 https://github.com/msiemens/tinydb
"""
from tinydb import TinyDB, Query

from yellowbot.storage.basestorageservice import BaseStorageService

class FilesystemStorageService(BaseStorageService):
    """Implement a StorageService using TinyDB, so using a simple file as a db
    """

    def __init__(self, file_name):
        """Initialize the class

        :param file_name: file name where data are persisted
        :type file_name: str
        """
        super().__init__()
        self._db = TinyDB(file_name)

    def save(self, document):
        """
        Insert a new document into the table.

        :param document: the document to insert
        :returns: the inserted document's ID
        :rtype:
        """
        self._db.insert(document)

    def search(self, cond):
        """
        Search for all documents matching a 'where' cond

        :param cond: the condition to check against
        :type cond: Query

        :return:
        :rtype: list[Element]
        """

        # Check code here: https://github.com/msiemens/tinydb/blob/master/tinydb/database.py
        return self._db.search(cond)

    def create_query(self):
        """
        Returns a query object to perform queries in the data
        :return:
        :rtype: Query
        """
        return Query()
