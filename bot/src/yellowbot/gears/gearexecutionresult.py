"""
"""

from typing import ClassVar, List, Optional


class GearExecutionResult:
    """Store information on the result of the operation of a gear
    """

    RESULT_OK: ClassVar[int] = 1
    RESULT_ERROR: ClassVar[int] = 2



    def __init__(
        self,
        result: int,
        messages: Optional[List[str]]=None
    ) -> None:
        self._result = result
        # message won't be None in any case
        self._messages = messages if messages is not None else []

    def get_messages(self) -> List[str]:
        """Returns the messages associated to the execution

        Worst case scenario, returns a list with 0 elements

        :returns: the execution messages
        :rtype: list[str]
        """

        return self._messages

    def has_messages(self) -> bool:
        """Checks if there are messages

        :returns: true if there is at least a message with a value
        :rtype: bool
        """

        return len(self._messages) > 0

    def get_result(self) -> int:
        """
        :returns: the result code of the execution
        :rtype: int
        """
        return self._result

    def went_well(self) -> bool:
        """Return how the execution went

        :returns: True if the task execution has a result code of RESULT_OK
        :rtype: bool
        """

        return self.RESULT_OK == self._result

    @staticmethod
    def OK(single_message: str = None) -> "GearExecutionResult":
        msg = []
        if single_message:
            msg.append(single_message)
        return GearExecutionResult(GearExecutionResult.RESULT_OK, msg)

    @staticmethod
    def ERROR(single_error_message: str = None) -> "GearExecutionResult":
        msg = []
        if single_error_message:
            msg.append(single_error_message)
        return GearExecutionResult(GearExecutionResult.RESULT_ERROR, msg)
