from typing import Any, override

from .action import AIRuleAction
from ..enums.action_code import ActionCode
from ..enums.global_event_table import GlobalEventTable
from ..enums.global_event import GlobalEvent


class SetGlobalEventFlagAction(AIRuleAction):
    def __init__(self, global_event_table_number: GlobalEventTable, mask: int) -> None:
        super().__init__(action_code=ActionCode.SET_GLOBAL_EVENT_FLAG, optional_second_byte=global_event_table_number.value, optional_third_byte=mask, optional_fourth_byte=None)

    @property
    def global_event_table_number(self) -> GlobalEventTable:
        if self.raw_second_byte is None:
            raise ValueError("Global event table number is not set.")
        else:
            return GlobalEventTable(self.raw_second_byte)

    @property
    def global_events_codes(self) -> list[GlobalEvent]:
        if self.raw_third_byte is None:
            raise ValueError("Global event mask is not set.")
        else:
            return GlobalEvent.from_table_and_mask(self.global_event_table_number, self.raw_third_byte)

    @property
    def global_events_names(self) -> list[str]:
        return [str(event) for event in self.global_events_codes]

    @override
    def to_json(self) -> str | dict[str, Any]:
        return {
            "action": self.action_code.name,
            "global_events": self.global_events_names
        }
