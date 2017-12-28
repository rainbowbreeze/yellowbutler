"""
Implement a datastore service

Currently it uses tinydb, but it's transparent to the outside world
"""
from tinydb import TinyDB, Query


class DatastoreService():
    """

    """

    def __init__(self, file_name):
        self._db = TinyDB(file_name)

    def write(self, document):
        """
        Insert a new document into the table.

        :param document: the document to insert
        :returns: the inserted document's ID
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
        """
        return Query()
