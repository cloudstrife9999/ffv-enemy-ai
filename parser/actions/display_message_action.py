from typing import Any, override

from .action import AIRuleAction
from ..enums.action_code import ActionCode


# TODO: Find out the mapping between the second and third bytes and the actual message that is displayed. For now, just store the raw values.
class DisplayMessageAction(AIRuleAction):
    def __init__(self, message_table_number: int, message_entry: int) -> None:
        super().__init__(action_code=ActionCode.DISPLAY_MESSAGE, optional_second_byte=message_table_number, optional_third_byte=message_entry, optional_fourth_byte=None)

    @property
    def message_table_number(self) -> int:
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
    def to_json(self) -> str | dict[str, Any]:
        return {
            "action": self.action_code.name,
            "message_table_number": self.message_table_number,
            "message_entry": self.message_entry
        }

    @override
    def to_compact_representation(self, indent: int) -> list[str]:
        return [f"{" " * indent}Display message {self.message_entry} from table {self.message_table_number}"]
