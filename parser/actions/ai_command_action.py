from typing import Any, override, cast

from .action import AIRuleAction
from ..enums.action_code import ActionCode


class AICommandAction(AIRuleAction):
    def __init__(self, sub_action: AIRuleAction) -> None:
        super().__init__(action_code=ActionCode.AI_COMMAND, optional_second_byte=sub_action.raw_action_code, optional_third_byte=sub_action.raw_second_byte, optional_fourth_byte=sub_action.raw_third_byte)

        self.__sub_action: AIRuleAction = sub_action

        if self.__sub_action.action_code is ActionCode.AI_COMMAND:
            raise ValueError("Infinite recursion is not allowed. AICommandAction cannot contain another AICommandAction as a sub-action.")
        elif self.__sub_action.action_code is ActionCode.RANDOM_SELECTION or self.__sub_action.action_code is ActionCode.GBA_RANDOM_SELECTION:
            raise ValueError("Random selection actions are not allowed as sub-actions of AICommandAction.")

    @property
    def sub_action(self) -> AIRuleAction:
        if self.raw_second_byte is None:
            raise ValueError("Sub-action is not set.")
        else:
            return self.__sub_action

    @override
    def to_json(self) -> str | dict[str, Any]:
        return {
            "action": "AI_COMMAND",  # TODO: workaround to avoid the 0xFD name collision with RANDOM_SELECTION, which is also 0xFD.
            **{self.__replace_action_key(k): v for k, v in cast(dict[str, Any], self.sub_action.to_json()).items()}
        }

    @staticmethod
    def __replace_action_key(key: str) -> str:
        if key == "action":
            return "type"
        else:
            return key

    @override
    def to_compact_representation(self, indent: int) -> list[str]:
        return [f"{" " * indent}AI command:"] + [f"{" " * indent}{line}" for line in self.sub_action.to_compact_representation(indent)]
