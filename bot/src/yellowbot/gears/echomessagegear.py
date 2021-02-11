"""
A YellowBot gear to echo a message

Requirements
- nothing
"""
from typing import Any, ClassVar, Dict, List, Optional
from yellowbot.gears.basegear import BaseGear
from yellowbot.gears.gearexecutionresult import GearExecutionResult
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
    ) -> GearExecutionResult:

        err_message = None
        if EchoMessageGear.INTENTS[0] != intent:
            err_message = "Call to {} using wrong intent {}".format(__name__, intent)
        if EchoMessageGear.PARAM_MESSAGE not in params:
            err_message = "Missing {} parameter in the request".format(EchoMessageGear.PARAM_MESSAGE)
        if err_message:
            self._logger.info(err_message)
            return GearExecutionResult.ERROR(err_message)

        # Very simply gear: return the message passed as input
        return GearExecutionResult.OK(params.get(EchoMessageGear.PARAM_MESSAGE))
