"""
A YellowBot gear to echo a message

Requirements
- nothing
"""
from yellowbot.gears.basegear import BaseGear
from yellowbot.globalbag import GlobalBag
from yellowbot.loggingservice import LoggingService


class EchoMessageGear(BaseGear):
    """
    Echo a message passed as parameter. Often use to check if the whole environment
    is setup properly
    """
    INTENTS = [GlobalBag.ECHO_MESSAGE_INTENT]
    PARAM_MESSAGE = GlobalBag.ECHO_MESSAGE_PARAM_MESSAGE  # The message to echo

    def __init__(self):
        super().__init__(self.__class__.__name__, self.INTENTS)
        self._logger = LoggingService.get_logger(__name__)

    def process_intent(self, intent, params):
        if EchoMessageGear.INTENTS[0] != intent:
            message = "Call to {} using wrong intent {}".format(__name__, intent)
            self._logger.info(message)
            return message 
        if EchoMessageGear.PARAM_MESSAGE not in params:
            return "Missing {} parameter in the request".format(EchoMessageGear.PARAM_MESSAGE)

        # Very simply gear: return the message passed as input
        return params.get(EchoMessageGear.PARAM_MESSAGE)
