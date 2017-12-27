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

    def __init__(self):
        BaseGear.__init__(self, MusicGear.__name__, self.INTENTS)

    def process_intent(self, intent, params):
        return "Sorry, I still don't know how to keep track of {} by {}".format(
            params[GlobalBag.TRACE_MUSIC_PARAM_TITLE],
            params[GlobalBag.TRACE_MUSIC_PARAM_AUTHOR]
        )

