
from typing import Any, override

from .action import AIRuleAction
from ..enums.action_code import ActionCode
from ..enums.gba_stats_and_properties_table import GBAStatsAndPropertiesTable
from ..enums.action_flags import ActionFlags
from ..enums.status import StatusCode
from ..enums.status_table import StatusTable


class GBAToggleStatusAction(AIRuleAction):
    def __init__(self, property_table: GBAStatsAndPropertiesTable, mask: int) -> None:
        super().__init__(action_code=ActionCode.SET_STATS_OR_TOGGLE_STATUS, optional_second_byte=property_table.value, optional_third_byte=mask, optional_fourth_byte=None)

    @property
    def property_table(self) -> GBAStatsAndPropertiesTable:
        if self.raw_second_byte is None:
            raise ValueError("The offset is not set.")
        else:
            return GBAStatsAndPropertiesTable(self.raw_second_byte)

    @property
    def mask(self) -> int:
        if self.raw_third_byte is None:
            raise ValueError("Mask is not set.")
        else:
            return self.raw_third_byte

    @override
    def terminates_turn_by_default(self) -> bool:
        return False

    @override
    def to_json(self) -> str | dict[str, Any]:
        if self.property_table == GBAStatsAndPropertiesTable.STATUS_1:
            status: StatusCode = StatusCode.from_table_and_mask(StatusTable.FIRST, self.mask)

            return {
                "action": str(self.action_code),
                "property_table": str(self.property_table),
                "status": str(status)
            }
        elif self.property_table == GBAStatsAndPropertiesTable.STATUS_2:
            status: StatusCode = StatusCode.from_table_and_mask(StatusTable.SECOND, self.mask)

            return {
                "action": str(self.action_code),
                "property_table": str(self.property_table),
                "status": str(status)
            }
        elif self.property_table == GBAStatsAndPropertiesTable.STATUS_3:
            status: StatusCode = StatusCode.from_table_and_mask(StatusTable.THIRD, self.mask)

            return {
                "action": str(self.action_code),
                "property_table": str(self.property_table),
                "status": str(status)
            }
        elif self.property_table == GBAStatsAndPropertiesTable.STATUS_4:
            status: StatusCode = StatusCode.from_table_and_mask(StatusTable.FOURTH, self.mask)

            return {
                "action": str(self.action_code),
                "property_table": str(self.property_table),
                "status": str(status)
            }
        elif self.property_table == GBAStatsAndPropertiesTable.ACTION_FLAGS:
            action_flags: ActionFlags = ActionFlags(self.mask)

            return {
                "action": str(self.action_code),
                "property_table": str(self.property_table),
                "action_flags": str(action_flags)
            }
        else:
            return {
                "action": str(self.action_code),
                "property_table": str(self.property_table),
                "mask": f"0x{self.mask:02X}",
            }

    @override
    def to_compact_representation(self, indent: int) -> list[str]:
        if self.property_table == GBAStatsAndPropertiesTable.STATUS_1:
            status: StatusCode = StatusCode.from_table_and_mask(StatusTable.FIRST, self.mask)

            return [f"{" " * indent}Toggle {str(status)} status."]
        elif self.property_table == GBAStatsAndPropertiesTable.STATUS_2:
            status: StatusCode = StatusCode.from_table_and_mask(StatusTable.SECOND, self.mask)

            return [f"{" " * indent}Toggle {str(status)} status."]
        elif self.property_table == GBAStatsAndPropertiesTable.STATUS_3:
            status: StatusCode = StatusCode.from_table_and_mask(StatusTable.THIRD, self.mask)

            return [f"{" " * indent}Toggle {str(status)} status."]
        elif self.property_table == GBAStatsAndPropertiesTable.STATUS_4:
            status: StatusCode = StatusCode.from_table_and_mask(StatusTable.FOURTH, self.mask)

            return [f"{" " * indent}Toggle {str(status)} status."]
        elif self.property_table == GBAStatsAndPropertiesTable.ACTION_FLAGS:
            action_flags: ActionFlags = ActionFlags(self.mask)

            return [f"{" " * indent}Set action flag: {str(action_flags)}."]
        else:
            return [f"{" " * indent}Set property {str(self.property_table)} to 0x{self.mask:02X}"]
