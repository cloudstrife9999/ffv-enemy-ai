from typing import Any, override

from .condition import AIRuleCondition
from ..enums.condition_code import ConditionCode
from ..enums.target import Target
from ..enums.status_table import StatusTable
from ..enums.status import StatusCode


class StatusEffectCondition(AIRuleCondition):
    def __init__(self, target: Target, status_table_number: StatusTable, mask: int) -> None:
        super().__init__(ConditionCode.STATUS_EFFECT.value, target.value, status_table_number.value, StatusCode.from_table_and_mask(status_table_number, mask).value[1])

    @property
    def target(self) -> Target:
        return Target(self.raw_second_byte)

    @property
    def status_table_number(self) -> StatusTable:
        return StatusTable(self.raw_third_byte)

    @property
    def status_code(self) -> StatusCode:
        return StatusCode.from_table_and_mask(self.status_table_number, self.raw_fourth_byte)

    @property
    def status_name(self) -> str:
        return str(self.status_code)

    @override
    def to_json(self) -> str | dict[str, Any]:
        return {
            "condition": str(self.condition_code),
            "target": str(self.target),
            "status_name": self.status_name
        }

    @override
    def to_compact_representation(self, indent: int) -> list[str]:
        if self.target is Target.SELF_UNLESS_FORCED:
            return [f"{" " * indent}Affected by the {self.status_name} status"]
        else:
            return [f"{" " * indent}{str(self.target)} {self.target.get_nominal_predicate()} affected by the {self.status_name} status"]
