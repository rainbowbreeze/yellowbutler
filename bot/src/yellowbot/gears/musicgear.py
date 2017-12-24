"""
Check for music

Requirements
- nothing
"""

from yellowbot.gears.basegear import BaseGear


class MusicGear(BaseGear):
    """
    Remember different kind of music
    """
    INTENTS = ["trace_music"]

    def __init__(self):
        BaseGear.__init__(self, "MusicGear", self.INTENTS)

    def process_intent(self, intent, params):
        return "Yeah!!!"
