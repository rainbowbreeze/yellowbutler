"""
A YellowBot gear to echo a message

Requirements
- nothing
"""
from yellowbot.gears.basegear import BaseGear
from yellowbot.globalbag import GlobalBag


class EchoMessageGear(BaseGear):
    """
    Echo a message passed as parameter. Often use to check if the whole environment
    is setup properly
    """
    INTENTS = [GlobalBag.ECHO_MESSAGE_INTENT]
    PARAM_MESSAGE = GlobalBag.ECHO_MESSAGE_PARAM_MESSAGE  # The message to echo

    def __init__(self):
        BaseGear.__init__(self, EchoMessageGear.__name__, self.INTENTS)

    def _check_parameters(self, params):
        return EchoMessageGear.PARAM_MESSAGE in params

    def process_intent(self, intent, params):
        if not self._check_parameters(params):
            raise ValueError("Cannot find one of the following parameters: {}".format(EchoMessageGear.PARAM_MESSAGE))

        # Very simply gear: return the message passed as input
        return params.get(EchoMessageGear.PARAM_MESSAGE)
