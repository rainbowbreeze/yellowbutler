"""
A YellowBot gear to echo a message

Requirements
- nothing
"""
from yellowbot.gears.basegear import BaseGear
from yellowbot.globalbag import GlobalBag


class EchoGear(BaseGear):
    """
    Echo a message passed as parameter. Often use to check if the whole environment
    is setup properly
    """
    INTENTS = [GlobalBag.ECHO_MESSAGE_INTENT]
    PARAM_MESSAGE = GlobalBag.ECHO_MESSAGE_PARAM_MESSAGE  # The message to echo

    def __init__(self):
        BaseGear.__init__(self, EchoGear.__name__, self.INTENTS)

    def _check_parameters(self, **params):
        return params.has_key(EchoGear.PARAM_MESSAGE)

    def process_intent(self, intent, params):
        return params.get(EchoGear.PARAM_MESSAGE)
