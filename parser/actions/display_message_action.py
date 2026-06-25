from typing import Any, override

from .action import AIRuleAction
from ..enums.action_code import ActionCode


class DisplayMessageAction(AIRuleAction):
    def __init__(self, unused_byte: int, message_entry: int, battle_text: dict[int, str]) -> None:
        super().__init__(action_code=ActionCode.DISPLAY_MESSAGE, optional_second_byte=unused_byte, optional_third_byte=message_entry, optional_fourth_byte=None)

        self.__battle_text: dict[int, str] = battle_text
        self.__message: str = self.__battle_text.get(message_entry, "Unknown message")

    @property
    def unused_byte(self) -> int:
        if self.raw_second_byte is None:
            raise ValueError("Message table number is not set.")
        else:
            return self.raw_second_byte

    @property
    def message_entry(self) -> int:
        if self.raw_third_byte is None:
            raise ValueError("Message entry is not set.")
        else:
            return self.raw_third_byte

    @override
    def terminates_turn_by_default(self) -> bool:
        return False

    @override
    def to_json(self) -> str | dict[str, Any]:
        return {
            "action": str(self.action_code),
            "message": self.__message if "\\n" not in self.__message else self.__message.split("\\n"),
            "unknown_parameter": f"0x{self.unused_byte:02X}",
            "entry": f"0x{self.message_entry:02X}"
        }

    @override
    def to_compact_representation(self, indent: int) -> list[str]:
        if "\\n" in self.__message:
            return [f'{" " * indent}Display message: {line}' for line in self.__message.split("\\n")]
        else:
            return [f'{" " * indent}Display message: {self.__message}']
