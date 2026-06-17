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
    def global_events_codes(self) -> list[GlobalEvent]:
        return GlobalEvent.from_table_and_mask(self.global_event_table_number, self.raw_fourth_byte)

    @property
    def global_events_names(self) -> list[str]:
        return [str(event) for event in self.global_events_codes]

    @override
    def to_json(self) -> str | dict[str, Any]:
        return {
            "condition": self.condition_code.name,
            "global_events": self.global_events_names
        }
