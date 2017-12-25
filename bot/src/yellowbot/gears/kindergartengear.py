"""
A YellowBot gear to check the kindergarten status and report it

Requirements
- nothing
"""

from yellowbot.gears.basegear import BaseGear
from yellowbot.globalbag import GlobalBag


class KindergartenGear(BaseGear):
    INTENTS = [
        GlobalBag.KINDERGARTEN_INTENT_CHECK,
        GlobalBag.KINDERGARTEN_INTENT_REPORT]

    def __init__(self):
        BaseGear.__init__(self, KindergartenGear.__name__, self.INTENTS)

    def process_intent(self, intent, params):
        return "Kindergarten subsystem here, at your command"
