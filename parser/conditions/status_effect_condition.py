from typing import Any, override

from .condition import AIRuleCondition
from ..enums.condition_code import ConditionCode
from ..enums.target import Target
from ..enums.status_table import StatusTable
from ..enums.status import StatusCode


class StatusEffectCondition(AIRuleCondition):
    def __init__(self, target: Target, status_table_number: StatusTable, mask: int) -> None:
        super().__init__(ConditionCode.STATUS_EFFECT.value, target.value, status_table_number.value, StatusCode.from_table_and_mask(status_table_number, mask).value)

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
            "condition": self.condition_code.name,
            "target": self.target.name,
            "status_name": self.status_name
        }
