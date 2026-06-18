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
        declared_length: int = cast(int, self.raw_second_byte)
        # We add back the 0xFD prefix from the AICommandAction.
        all_tokens: list[int] = [0xFD] + self.get_tokens() + [token for action in self.sub_actions for token in action.get_tokens()] # Exclude the tokens of the actual NoInterruptAction itself (4 bytes)

        if cumulative_length != declared_length and override_length_mismatch:
            print(f"[Parser] Warning: NoInterruptAction declared length ({declared_length}) does not match the cumulative length of sub-actions ({cumulative_length}). This mismatch is being overridden.")
            print(f"[Parser] The cumulative length {"includes" if self.__separator_or_terminator_included_in_length else "does not include"} an additional byte due to the separator/terminator being included.")
            print(f"[Parser] NoInterruptAction tokens (excluding a potential final separator/terminator): {" ".join(f"{b:02X}" for b in all_tokens)}.")
        elif cumulative_length != declared_length:
            raise ValueError(f"Sub-actions cumulative length ({cumulative_length}) does not match the specified limit ({declared_length}). An additional byte for a separator or terminator was {"included" if self.__separator_or_terminator_included_in_length else "not included"} in the cumulative length.")

    @override
    def terminates_turn_by_default(self) -> bool:
        return True

    @override
    def to_json(self) -> str | dict[str, Any]:
        return {
            "action": self.action_code.name,
            "sub_actions": [action.to_json() for action in self.sub_actions]
        }

    @override
    def to_compact_representation(self, indent: int) -> list[str]:
        return [f"{" " * indent}Consecutive actions:"] + [f"{" " * indent}{line}" for action in self.sub_actions for line in action.to_compact_representation(indent)]