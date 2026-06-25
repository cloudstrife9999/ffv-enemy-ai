from typing import Any, override

from .condition import AIRuleCondition
from ..enums.condition_code import ConditionCode
from ..enums.target import Target
from ..enums.snes_stats_and_properties_table import SNESStatsAndPropertiesTable
from ..enums.command_status import CommandStatus


class SNESStatOrPropertyCondition(AIRuleCondition):
    def __init__(self, target: Target, property_table: SNESStatsAndPropertiesTable, expected_value: int) -> None:
        super().__init__(ConditionCode.STAT_OR_PROPERTY.value, target.value, property_table.value, expected_value)

    @property
    def target(self) -> Target:
        return Target(self.raw_second_byte)

    @property
    def stats_and_properties_table(self) -> SNESStatsAndPropertiesTable:
        return SNESStatsAndPropertiesTable(self.raw_third_byte)

    @property
    def expected_value(self) -> int:
        return self.raw_fourth_byte

    @override
    def to_json(self) -> str | dict[str, Any]:
        return {
            "condition_code": self.condition_code.name,
            "target": self.target.name,
            "stats_and_properties_table": self.stats_and_properties_table.name,
            "expected_value": self.expected_value
        } if self.stats_and_properties_table != SNESStatsAndPropertiesTable.CMD_STATUS else {
            "condition_code": self.condition_code.name,
            "target": self.target.name,
            "stats_and_properties_table": self.stats_and_properties_table.name,
            "command_status": CommandStatus(self.expected_value).name
        }

    @override
    def to_compact_representation(self, indent: int) -> list[str]:
        if self.stats_and_properties_table == SNESStatsAndPropertiesTable.CMD_STATUS:
            return [f"{" " * indent}Stat/Property {str(self.stats_and_properties_table)} is \"{str(CommandStatus(self.expected_value))}\" for {self.target.for_mid_sentence()}"]
        else:
            return [f"{" " * indent}Stat/Property {str(self.stats_and_properties_table)} is {self.expected_value} for {self.target.for_mid_sentence()}"]
