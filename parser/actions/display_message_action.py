from typing import Any, override

from .action import AIRuleAction
from ..enums.action_code import ActionCode


class DisplayMessageAction(AIRuleAction):
    def __init__(self, message_table_number: int, message_entry: int) -> None:
        super().__init__(action_code=ActionCode.DISPLAY_MESSAGE, optional_second_byte=message_table_number, optional_third_byte=message_entry, optional_fourth_byte=None)

    @property
    def message_table_number(self) -> int:
        if not self.raw_second_byte:
            raise ValueError("Message table number is not set.")
        else:
            return self.raw_second_byte

    @property
    def message_entry(self) -> int:
        if not self.raw_third_byte:
            raise ValueError("Message entry is not set.")
        else:
            return self.raw_third_byte

    @override
    def to_json(self) -> str | dict[str, Any]:
        return {
            "action": self.action_code.name,
            "message_table_number": self.message_table_number,
            "message_entry": self.message_entry
        }
