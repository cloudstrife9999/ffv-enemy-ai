from typing import Any, override

from .condition import AIRuleCondition
from ..enums.condition_code import ConditionCode
from ..enums.target import Target
from ..enums.party_member_offset import PartyMemberPropertyTable
from ..enums.command_status import CommandStatus


class PartyMemberParameterCondition(AIRuleCondition):
    def __init__(self, target: Target, property_table: PartyMemberPropertyTable, expected_value: int) -> None:
        super().__init__(ConditionCode.PARTY_MEMBER_PARAMETER.value, target.value, property_table.value, expected_value)

    @property
    def target(self) -> Target:
        return Target(self.raw_second_byte)

    @property
    def property_table(self) -> PartyMemberPropertyTable:
        return PartyMemberPropertyTable(self.raw_third_byte)

    @property
    def expected_value(self) -> int:
        return self.raw_fourth_byte

    @override
    def to_json(self) -> str | dict[str, Any]:
        return {
            "condition_code": self.condition_code.name,
            "target": self.target.name,
            "property_table": self.property_table.name,
            "expected_value": self.expected_value
        } if self.property_table != PartyMemberPropertyTable.CMD_STATUS else {
            "condition_code": self.condition_code.name,
            "target": self.target.name,
            "property_table": self.property_table.name,
            "command_status": CommandStatus(self.expected_value).name
        }

    @override
    def to_compact_representation(self, indent: int) -> list[str]:
        if self.property_table == PartyMemberPropertyTable.CMD_STATUS:
            return [f"{" " * indent}Property {str(self.property_table)} is \"{str(CommandStatus(self.expected_value))}\" for {self.target.for_mid_sentence()}"]
        else:
            return [f"{" " * indent}Property {str(self.property_table)} is {self.expected_value} for {self.target.for_mid_sentence()}"]
