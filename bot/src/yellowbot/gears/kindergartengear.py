"""
A YellowBot gear to check the kindergarten status and report it

Requirements
- nothing
"""

from yellowbot.gears.basegear import BaseGear


class KindergartenGear(BaseGear):
    INTENTS = [
        "kindergarten_report_last_status",
        "kindergarten_check"]

    def __init__(self):
        BaseGear.__init__(self, "KindergartenGear", self.INTENTS)

    def process_intent(self, intent, params):
        return "Kindergarten subsystem here, at your command"
