
from typing import Any, override

from .action import AIRuleAction
from ..enums.action_code import ActionCode


class UnknownF5Action(AIRuleAction):
    def __init__(self, second_byte: int, third_byte: int) -> None:
        super().__init__(action_code=ActionCode.UNKNOWN_F5_ACTION, optional_second_byte=second_byte, optional_third_byte=third_byte, optional_fourth_byte=None)

    @property
    def second_byte(self) -> int:
        if self.raw_second_byte is None:
            raise ValueError("Second byte is not set.")
        else:
            return self.raw_second_byte

    @property
    def third_byte(self) -> int:
        if self.raw_third_byte is None:
            raise ValueError("Third byte is not set.")
        else:
            return self.raw_third_byte

    @override
    def terminates_turn_by_default(self) -> bool:
        return False

    @override
    def to_json(self) -> str | dict[str, Any]:
        return {
            "action": self.action_code.name,
            "second_byte": self.second_byte,
            "third_byte": self.third_byte
        }

    @override
    def to_compact_representation(self, indent: int) -> list[str]:
        return [f"{" " * indent}An unknown action (0xF5)"]
