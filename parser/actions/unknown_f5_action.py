
from typing import Any, override

from .action import AIRuleAction
from ..enums.action_code import ActionCode


# TODO: find out what this action actually does.
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
            "action": str(self.action_code),
            "second_byte": f"0x{self.second_byte:02X}",
            "third_byte": f"0x{self.third_byte:02X}"
        }

    @override
    def to_compact_representation(self, indent: int) -> list[str]:
        return [f"{" " * indent}An unknown action [0xFD 0xF5 0x{self.second_byte:02X} 0x{self.third_byte:02X}]"]
