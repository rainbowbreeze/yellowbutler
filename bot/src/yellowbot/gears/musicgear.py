"""
A YellowBot gear to add title and artist of a song to a Google Spreadsheet

Requirements
- requests
"""
from typing import Any, ClassVar, Dict, List, Optional
import requests

from yellowbot.gears.basegear import BaseGear
from yellowbot.gears.gearexecutionresult import GearExecutionResult
from yellowbot.globalbag import GlobalBag
from yellowbot.loggingservice import LoggingService


class MusicGear(BaseGear):
    """
    Remember different kind of music
    """
    INTENTS: ClassVar[List[str]] = [GlobalBag.TRACE_MUSIC_INTENT]
    PARAM_TITLE: ClassVar[str] = GlobalBag.TRACE_MUSIC_PARAM_TITLE
    PARAM_AUTHOR: ClassVar[str]  = GlobalBag.TRACE_MUSIC_PARAM_AUTHOR

    def __init__(
        self,
        destination_url: str,
        test_mode:bool = False
    ) -> None:
        """

        :param destination_url: url where send the author and title
        :type destination_url: str

        :param test_mode: class instance created for test purposes, some
        features are disabled
        :type test_mode: bool
        """
        super().__init__(self.__class__.__name__, self.INTENTS)
        self._logger = LoggingService.get_logger(__name__)
        self._destination_url = destination_url
        self._test_mode = test_mode

    def process_intent(
        self,
        intent: str,
        params: Dict[str, Any]
    ) -> GearExecutionResult:
        """
        """

        err_message = None
        if MusicGear.INTENTS[0] != intent:
            err_message = "Call to {} using wrong intent {}".format(__name__, intent)
        if MusicGear.PARAM_TITLE not in params:
            err_message = "Missing {} parameter in the request".format(MusicGear.PARAM_TITLE)
        if MusicGear.PARAM_AUTHOR not in params:
            err_message = "Missing {} parameter in the request".format(MusicGear.PARAM_AUTHOR)
        if err_message:
            return GearExecutionResult.ERROR(err_message)

        # Send the data at given url as form request
        author = params[MusicGear.PARAM_AUTHOR]
        title = params[MusicGear.PARAM_TITLE]
        data = {
            'Author': author,
            'Title': title
        }

        if self._test_mode:
            return GearExecutionResult.OK("{} by {} has been added".format(title, author))

        try:
            self._logger.info("Sending music trace request to url {}".format(self._destination_url))
            response = requests.post(self._destination_url, data)
            if response.ok:
                # Sometimes 200 is returned even if there is an error of some sort
                # Because this code is very generic, send a form data to an
                #  url, a custom check needs to be performed to be really
                #  sure about the response validity. For now, just check
                #  the OK status codes range
                message = "{} by {} has been added".format(title, author)
                self._logger.debug(message)
                return GearExecutionResult.OK(message)
            else:
                message = "Error adding the song: status {}, {}".format(response.status_code, response.text)
                self._logger.info(message)
                return GearExecutionResult.OK(message)
        except Exception as err:
            error_message = "An error happened while adding the song: {}".format(err)
            self._logger.exception(error_message)
            return GearExecutionResult.ERROR(error_message)
