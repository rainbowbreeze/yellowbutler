"""
A YellowBot gear to check for music

Requirements
- nothing
"""

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

    def __init__(self):
        BaseGear.__init__(self, MusicGear.__name__, self.INTENTS)
        self._logger = LoggingService.get_logger(__name__)

    def process_intent(self, intent, params):
        if MusicGear.PARAM_TITLE not in params:
            return "Missing {} parameter in the request".format(MusicGear.PARAM_TITLE)
        if MusicGear.PARAM_AUTHOR not in params:
            return "Missing {} parameter in the request".format(MusicGear.PARAM_AUTHOR)

        return "Sorry, I still don't know how to keep track of {} by {}".format(
            params[MusicGear.PARAM_TITLE],
            params[MusicGear.PARAM_AUTHOR]
        )
