from typing import Any, override

from .action import AIRuleAction
from ..enums.action_code import ActionCode


class NoInterruptAction(AIRuleAction):
    def __init__(self, sub_actions_cumulative_length: int, third_byte: int, sub_actions: list[AIRuleAction], length_includes_separator_or_terminator: bool) -> None:
        super().__init__(action_code=ActionCode.NO_INTERRUPT, optional_second_byte=sub_actions_cumulative_length, optional_third_byte=third_byte, optional_fourth_byte=None)

        self.__sub_actions: list[AIRuleAction] = sub_actions
        self.__length_includes_separator_or_terminator: bool = length_includes_separator_or_terminator

        additional_length: int = 1 if length_includes_separator_or_terminator else 0

        if len(sub_actions) < 2:
            raise ValueError("A NoInterruptAction must have at least two sub-actions.")

        if sub_actions_cumulative_length != sum(action.length for action in sub_actions) + additional_length:
            raise ValueError("The provided sub_actions_cumulative_length does not match the sum of the lengths of the provided sub-actions (taking into account the potential additional separator/terminator).")

    @property
    def sub_actions(self) -> list[AIRuleAction]:
        if not self.__sub_actions:
            raise ValueError("Sub-actions are not set.")
        else:
            return self.__sub_actions

    @property
    def sub_actions_cumulative_length(self) -> int:
        if not self.raw_second_byte:
            raise ValueError("Sub-actions cumulative length is not set.")
        else:
            return self.raw_second_byte

    @property
    def length_includes_separator_or_terminator(self) -> bool:
        return self.__length_includes_separator_or_terminator

    @override
    def to_json(self) -> str | dict[str, Any]:
        return {
            "action": self.action_code.name,
            "sub_actions": [action.to_json() for action in self.sub_actions]
        }
