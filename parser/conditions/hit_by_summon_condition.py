from typing import Any, override

from .condition import AIRuleCondition
from ..enums.condition_code import ConditionCode


class HitBySummonCondition(AIRuleCondition):
    def __init__(self, second_byte: int, third_byte: int, fourth_byte: int) -> None:
        super().__init__(ConditionCode.HIT_BY_SUMMON.value, second_byte, third_byte, fourth_byte)

    @override
    def to_json(self) -> str | dict[str, Any]:
        return self.condition_code.name
