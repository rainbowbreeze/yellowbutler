"""A YellowBot gear to read latest CommitStrip artwork and output the one for the current day

Requirements
-requests
-feedparser
-arrow
"""

from typing import Any, ClassVar, Dict, List, Optional
from arrow import Arrow
import feedparser
import re
import requests
import arrow

from yellowbot.gears.basegear import BaseGear
from yellowbot.gears.gearexecutionresult import GearExecutionResult
from yellowbot.globalbag import GlobalBag
from yellowbot.loggingservice import LoggingService

class CommitStripGear(BaseGear):
    """Read the CommitStrip RSS and check if there is a new artwork with the same date of today
    """

    INTENTS: ClassVar[List[str]] = [GlobalBag.COMMITSTRIP_INTENT]
    PARAM_SILENT: ClassVar[str] = GlobalBag.COMMITSTRIP_PARAM_SILENT  # No notification if there is nothing new 

    def __init__(self):
        super().__init__(self.__class__.__name__, self.INTENTS)
        self._logger = LoggingService.get_logger(__name__)

    def process_intent(
        self,
        intent: str,
        params: Dict[str, Any]
    ) -> GearExecutionResult:
        if CommitStripGear.INTENTS[0] != intent:
            err_message = "Call to {} using wrong intent {}".format(__name__, intent)
            self._logger.info(err_message)
            return GearExecutionResult.ERROR(err_message) 

        # Defaul value for silent param
        silent = False
        if CommitStripGear.PARAM_SILENT in params:
            silent = params[CommitStripGear.PARAM_SILENT]

        result = self._find_daily_strip(silent)
        return GearExecutionResult.OK(result)

    def _find_daily_strip(self, silent: bool) -> Optional[str]:
        """Read CommitStrip RSS, extract latest Strips and check if there is something for today

        :param silent: if True, doesn't produce any value when new content is not found
        :type silent: bool

        :returns: a message with the result of the processing
        :rtype: str
        """

        # First, get the RSS feed from CommitStrip website
        try:
            req = requests.get("http://www.commitstrip.com/en/feed/")
            if not req.ok:
                req.raise_for_status()
            rssdata = req.text
        except BaseException as err:
            error_message = "Error while reading RSS feed from CommitStrip: {}".format(err)
            self._logger.exception(error_message)
            return error_message
        
        today = arrow.utcnow()
        return self._get_strip_for_date(rssdata, today, silent)

    def _get_strip_for_date(
        self,
        rss_content: str,
        date_to_compare: Arrow,
        silent: bool) -> Optional[str]:
        """Parse the RSS stream and check if the most recent item was published on the same date of the specific data param

        :param rss_content: the RSS content output of CommitStrip
        :type rss_content: str

        :param date_to_compare: the day CommitStrip should have published something
        :type date_to_compare: arrow

        :param silent: do not send any message if there is a new strip for the given date
        :type silent: boolean

        :returns: None, or the url of the image published in the specified day
        :rtype: str

        :raises: Error not catched here, are catched in the process intent method
        """

        if not rss_content:
          return None

        d = feedparser.parse(rss_content)
        # return d.feed.title
      
        # Follow the approach EAFP (Easier to ask forgiveness than permission -
        #  https://docs.python.org/3/glossary.html#term-eafp)
        try:
            # Analyze only the first element of the RSS strean
            first_entry = d.entries[0]
            published = first_entry.dc_modified

            strip_published_date = arrow.get(published)
            if date_to_compare.format("YYYY-MM-DD") == strip_published_date.format("YYYY-MM-DD"):
                # Bingo, latest strip in the RSS stream was published for the date specified 
                # Get the info for the first element of the RSS
                img_tag = first_entry.content[0].value
                # <img src="https://www.commitstrip.com/wp-content/uploads/2020/01/Strip-Paywall-650-finalenglish.jpg" alt="" width="650" height="607" class="alignnone size-full wp-image-20822" />
                img_matches = re.search('src="([^"]+)"', img_tag)
                return "New CommitStrip content: {}\n{}".format(
                    first_entry.title,
                    img_matches[1]
                )
            elif not silent:
                return "No new CommitStrip for today"
            else:
                return None
        except Exception as err:
            # It could be
            # - IndexError if there are no items inside the main feed definition
            err_message = "Something wrong has appened in parsing RSS Data: {}".format(err)
            self._logger.exception(err_message)
            return err_message



