from typing import Any, override, cast

from .action import AIRuleAction
from ..enums.action_code import ActionCode


class NoInterruptAction(AIRuleAction):
    def __init__(self, sub_actions_cumulative_length: int, third_byte: int) -> None:
        super().__init__(action_code=ActionCode.NO_INTERRUPT, optional_second_byte=sub_actions_cumulative_length, optional_third_byte=third_byte, optional_fourth_byte=None)

        self.__sub_actions: list[AIRuleAction] = []
        self.__separator_or_terminator_included_in_length: bool = False

    @property
    def sub_actions(self) -> list[AIRuleAction]:
        if not self.__sub_actions:
            raise ValueError("Sub-actions are not set.")
        else:
            return self.__sub_actions

    @property
    def sub_actions_cumulative_length(self) -> int:
        if self.raw_second_byte is None:
            raise ValueError("Sub-actions cumulative length is not set.")
        else:
            return self.raw_second_byte

    def add_sub_action(self, sub_action: AIRuleAction) -> None:
        self.__sub_actions.append(sub_action)

        cumulative_length: int = sum(len(sub_action.get_tokens()) for sub_action in self.__sub_actions)

        if cumulative_length > cast(int, self.raw_second_byte):
            raise ValueError(f"Sub-actions cumulative length ({cumulative_length}) exceeds the specified limit ({self.raw_second_byte}).")

    def mark_separator_or_terminator_included_in_length(self) -> None:
        self.__separator_or_terminator_included_in_length = True

    def validate_complete_action(self, override_length_mismatch: bool = False) -> None:
        if len(self.sub_actions) < 2:
            raise ValueError("A NoInterruptAction must contain at least two sub-actions.")

        cumulative_length: int = sum(len(sub_action.get_tokens()) for sub_action in self.__sub_actions) + (1 if self.__separator_or_terminator_included_in_length else 0)

        if override_length_mismatch:
            print(f"Warning: Overriding length mismatch. Sub-actions cumulative length ({cumulative_length}) does not match the specified limit ({self.raw_second_byte}). An additional byte for a separator or terminator was {'included' if self.__separator_or_terminator_included_in_length else 'not included'} in the cumulative length.")
        elif cumulative_length != cast(int, self.raw_second_byte):
            raise ValueError(f"Sub-actions cumulative length ({cumulative_length}) does not match the specified limit ({self.raw_second_byte}). An additional byte for a separator or terminator was {"included" if self.__separator_or_terminator_included_in_length else "not included"} in the cumulative length.")

    @override
    def to_json(self) -> str | dict[str, Any]:
        return {
            "action": self.action_code.name,
            "sub_actions": [action.to_json() for action in self.sub_actions]
        }
