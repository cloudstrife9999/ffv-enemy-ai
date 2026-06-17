
from typing import Any, override

from .action import AIRuleAction
from ..enums.action_code import ActionCode
from ..enums.party_member_offset import PartyMemberPropertyTable
from ..enums.command_status import CommandStatus


class SetStatsOrToggleStatusAction(AIRuleAction):
    def __init__(self, property_table: PartyMemberPropertyTable, mask: int) -> None:
        super().__init__(action_code=ActionCode.SET_STATS_OR_TOGGLE_STATUS, optional_second_byte=property_table.value, optional_third_byte=mask, optional_fourth_byte=None)

    @property
    def property_table(self) -> PartyMemberPropertyTable:
        if self.raw_second_byte is None:
            raise ValueError("Party member offset is not set.")
        else:
            return PartyMemberPropertyTable(self.raw_second_byte)

    @property
    def mask(self) -> int:
        if self.raw_third_byte is None:
            raise ValueError("Mask is not set.")
        else:
            return self.raw_third_byte

    @override
    def to_json(self) -> str | dict[str, Any]:
        return {
            "action": self.action_code.name,
            "property_table": self.property_table.name,
            "mask": self.mask,
        } if self.property_table != PartyMemberPropertyTable.CMD_STATUS else {
            "action": self.action_code.name,
            "property_table": self.property_table.name,
            "command_status": CommandStatus(self.mask).name
        }
