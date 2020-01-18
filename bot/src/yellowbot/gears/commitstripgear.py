"""
A YellowBot gear to read latest CommitStrip artwork and output the one for the current day

Requirements
-requests
-feedparser
"""

import feedparser

from yellowbot.gears.basegear import BaseGear
from yellowbot.globalbag import GlobalBag
from yellowbot.loggingservice import LoggingService

class CommitStripGear(BaseGear):
    """
    Read the CommitStrip RSS and check if there is a new artwork with the same date of today
    """
    INTENTS = [GlobalBag.COMMITSTRIP_INTENT]

    def __init__(self):
        BaseGear.__init__(self, CommitStripGear.__name__, self.INTENTS)
        self._logger = LoggingService.get_logger(__name__)

    def process_intent(self, intent, params):
        if CommitStripGear.INTENTS[0] != intent:
            message = "Call to {} using wrong intent {}".format(__name__, intent)
            self._logger.info(message)
            return message 

        return self._read_daily_commitstrip

    def _read_daily_commitstrip(self):
        """
        Read CommitStrip RSS, extract latest Strips and check if there is something for today
        """

    def _return_latest_strip(self, rssoutput):
        """
        Parse the RSS stream and return the most recent strip
        """
        if not rssoutput:
          return None

        d = feedparser.parse(rssoutput)
        # return d.feed.title
      
        # Follow the approach EAFP (Easier to ask forgiveness than permission -
        #  https://docs.python.org/3/glossary.html#term-eafp)
        try:
            first_entry = d.entries[0]
            if "published" not in first_entry:
                return None
            published = first_entry.published

            return published
        except IndexError:
            return None



