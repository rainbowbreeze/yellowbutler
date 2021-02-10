"""
A YellowBot gear to echo a message

Requirements
- nothing
"""
from typing import Any, ClassVar, Dict, List, Optional
from yellowbot.gears.basegear import BaseGear
from yellowbot.globalbag import GlobalBag
from yellowbot.loggingservice import LoggingService


class EchoMessageGear(BaseGear):
    """
    Echo a message passed as parameter. Often use to check if the whole environment
    is setup properly
    """
    INTENTS: ClassVar[List[str]] = [GlobalBag.ECHO_MESSAGE_INTENT]
    PARAM_MESSAGE: ClassVar[str] = GlobalBag.ECHO_MESSAGE_PARAM_MESSAGE  # The message to echo

    def __init__(self) -> None:
        super().__init__(self.__class__.__name__, self.INTENTS)
        self._logger = LoggingService.get_logger(__name__)

    def process_intent(
        self,
        intent: str,
        params: Dict[str, Any]
    ) -> Optional[str]:
        if EchoMessageGear.INTENTS[0] != intent:
            message = "Call to {} using wrong intent {}".format(__name__, intent)
            self._logger.info(message)
            return message 
        if EchoMessageGear.PARAM_MESSAGE not in params:
            return "Missing {} parameter in the request".format(EchoMessageGear.PARAM_MESSAGE)

        # Very simply gear: return the message passed as input
        return params.get(EchoMessageGear.PARAM_MESSAGE)
