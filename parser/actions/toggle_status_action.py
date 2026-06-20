
from typing import Any, override

from .action import AIRuleAction
from ..enums.action_code import ActionCode
from ..enums.stats_and_properties_table import StatsAndPropertiesTable
from ..enums.command_status import CommandStatus
from ..enums.status import StatusCode
from ..enums.status_table import StatusTable


class ToggleStatusAction(AIRuleAction):
    def __init__(self, property_table: StatsAndPropertiesTable, mask: int) -> None:
        super().__init__(action_code=ActionCode.SET_STATS_OR_TOGGLE_STATUS, optional_second_byte=property_table.value, optional_third_byte=mask, optional_fourth_byte=None)

    @property
    def property_table(self) -> StatsAndPropertiesTable:
        if self.raw_second_byte is None:
            raise ValueError("Party member offset is not set.")
        else:
            return StatsAndPropertiesTable(self.raw_second_byte)

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
        if self.property_table == StatsAndPropertiesTable.STATUS_1:
            status: StatusCode = StatusCode.from_table_and_mask(StatusTable.FIRST, self.mask)

            return {
                "action": self.action_code.name,
                "property_table": self.property_table.name,
                "status": status.name
            }
        elif self.property_table == StatsAndPropertiesTable.STATUS_2:
            status: StatusCode = StatusCode.from_table_and_mask(StatusTable.SECOND, self.mask)

            return {
                "action": self.action_code.name,
                "property_table": self.property_table.name,
                "status": status.name
            }
        elif self.property_table == StatsAndPropertiesTable.STATUS_3:
            status: StatusCode = StatusCode.from_table_and_mask(StatusTable.THIRD, self.mask)

            return {
                "action": self.action_code.name,
                "property_table": self.property_table.name,
                "status": status.name
            }
        elif self.property_table == StatsAndPropertiesTable.STATUS_4:
            status: StatusCode = StatusCode.from_table_and_mask(StatusTable.FOURTH, self.mask)

            return {
                "action": self.action_code.name,
                "property_table": self.property_table.name,
                "status": status.name
            }
        elif self.property_table == StatsAndPropertiesTable.CMD_STATUS:
            command_status: CommandStatus = CommandStatus(self.mask)

            return {
                "action": self.action_code.name,
                "property_table": self.property_table.name,
                "command_status": command_status.name
            }
        else:
            return {
                "action": self.action_code.name,
                "property_table": self.property_table.name,
                "mask": self.mask,
            }

    @override
    def to_compact_representation(self, indent: int) -> list[str]:
        if self.property_table == StatsAndPropertiesTable.STATUS_1:
            status: StatusCode = StatusCode.from_table_and_mask(StatusTable.FIRST, self.mask)

            return [f"{" " * indent}Toggle {str(status)} status."]
        elif self.property_table == StatsAndPropertiesTable.STATUS_2:
            status: StatusCode = StatusCode.from_table_and_mask(StatusTable.SECOND, self.mask)

            return [f"{" " * indent}Toggle {str(status)} status."]
        elif self.property_table == StatsAndPropertiesTable.STATUS_3:
            status: StatusCode = StatusCode.from_table_and_mask(StatusTable.THIRD, self.mask)

            return [f"{" " * indent}Toggle {str(status)} status."]
        elif self.property_table == StatsAndPropertiesTable.STATUS_4:
            status: StatusCode = StatusCode.from_table_and_mask(StatusTable.FOURTH, self.mask)

            return [f"{" " * indent}Toggle {str(status)} status."]
        elif self.property_table == StatsAndPropertiesTable.CMD_STATUS:
            command_status: CommandStatus = CommandStatus(self.mask)

            return [f"{" " * indent}Set command status to {str(command_status)}."]
        else:
            return [f"{" " * indent}Set property {str(self.property_table)} to {self.mask:#04x}"]
