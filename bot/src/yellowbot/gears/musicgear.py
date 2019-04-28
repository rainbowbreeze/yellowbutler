"""
A YellowBot gear to add title and artist of a song to a Google Spreadsheet

Requirements
- requests
"""
import requests

from yellowbot.gears.basegear import BaseGear
from yellowbot.globalbag import GlobalBag
from yellowbot.loggingservice import LoggingService


class MusicGear(BaseGear):
    """
    Remember different kind of music
    """
    INTENTS = [GlobalBag.TRACE_MUSIC_INTENT]
    PARAM_TITLE = GlobalBag.TRACE_MUSIC_PARAM_TITLE
    PARAM_AUTHOR = GlobalBag.TRACE_MUSIC_PARAM_AUTHOR

    def __init__(self,
                 destination_url,
                 test_mode=False):
        """

        :param destination_url: url where send the author and title
        :type destination_url: str

        :param test_mode: class instance created for test purposes, some
        features are disabled
        :type test_mode: bool
        """
        BaseGear.__init__(self, MusicGear.__name__, self.INTENTS)
        self._logger = LoggingService.get_logger(__name__)
        self._destination_url = destination_url
        self._test_mode = test_mode

    def process_intent(self, intent, params):
        if MusicGear.INTENTS[0] != intent:
            message = "Call to {} using wrong intent {}".format(__name__, intent)
            self._logger.info(message)
            return message
        if MusicGear.PARAM_TITLE not in params:
            return "Missing {} parameter in the request".format(MusicGear.PARAM_TITLE)
        if MusicGear.PARAM_AUTHOR not in params:
            return "Missing {} parameter in the request".format(MusicGear.PARAM_AUTHOR)

        # Send the data at given url as form request
        author = params[MusicGear.PARAM_AUTHOR]
        title = params[MusicGear.PARAM_TITLE]
        data = {
            'Author': author,
            'Title': title
        }

        if self._test_mode:
            return "{} by {} has been added".format(title, author)

        try:
            self._logger.info("Sending music trace request to url {}".format(self._destination_url))
            response = requests.post(self._destination_url, data)
            if response.ok:
                # Sometimes 200 is returned even if there is an error of some sort
                # Because this code is very generic, send a form data to an
                #  url, a custom check needs to be performed to be really
                #  sure about the response validity. For now, just check
                #  the OK status codes range
                return "{} by {} has been added".format(title, author)
            else:
                return "Error adding the song: status {}, {}".format(response.status_code, response.text)
        except Exception as e:
            self._logger.exception(e)
            return "An error happened while adding the song: {}".format(repr(e))
