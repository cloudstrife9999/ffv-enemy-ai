from typing import Any, override

from .condition import AIRuleCondition
from ..enums.condition_code import ConditionCode
from ..enums.global_event_table import GlobalEventTable
from ..enums.global_event import GlobalEvent


class GlobalEventCondition(AIRuleCondition):
    def __init__(self, second_byte: int, global_event_table_number: GlobalEventTable, mask: int) -> None:
        super().__init__(ConditionCode.GLOBAL_EVENT_FLAGS.value, second_byte, global_event_table_number.value, mask)

    @property
    def global_event_table_number(self) -> GlobalEventTable:
        return GlobalEventTable(self.raw_third_byte)

    @property
    def global_event_code(self) -> GlobalEvent:
        return GlobalEvent.from_table_and_mask(self.global_event_table_number, self.raw_fourth_byte)

    @property
    def global_event_name(self) -> str:
        return str(self.global_event_code)

    @override
    def to_json(self) -> str | dict[str, Any]:
        return {
            "condition": self.condition_code.name,
            "global_event": self.global_event_name
        }
