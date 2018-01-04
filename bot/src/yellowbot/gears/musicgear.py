"""
A YellowBot gear to check for music

Requirements
- nothing
"""

from yellowbot.gears.basegear import BaseGear
from yellowbot.globalbag import GlobalBag


class MusicGear(BaseGear):
    """
    Remember different kind of music
    """
    INTENTS = [GlobalBag.TRACE_MUSIC_INTENT]
    PARAM_TITLE = GlobalBag.TRACE_MUSIC_PARAM_TITLE
    PARAM_AUTHOR = GlobalBag.TRACE_MUSIC_PARAM_AUTHOR

    def __init__(self):
        BaseGear.__init__(self, MusicGear.__name__, self.INTENTS)

    def _check_parameters(self, params):
        return MusicGear.PARAM_AUTHOR in params and MusicGear.PARAM_TITLE in params

    def process_intent(self, intent, params):
        return "Sorry, I still don't know how to keep track of {} by {}".format(
            params[MusicGear.PARAM_TITLE],
            params[MusicGear.PARAM_AUTHOR]
        )
