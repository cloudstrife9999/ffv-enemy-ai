from typing import Any, override

from .condition import AIRuleCondition
from ..enums.condition_code import ConditionCode


class A2ComparisonCondition(AIRuleCondition):
    def __init__(self, second_byte: int, value_lsb: int, value_msb: int) -> None:
        super().__init__(ConditionCode.COMPARE_WITH_A2.value, second_byte, value_lsb, value_msb)

    @property
    def value(self) -> int:
        return (self.raw_fourth_byte << 8) | self.raw_third_byte

    @override
    def to_json(self) -> str | dict[str, Any]:
        return {
            "condition": self.condition_code.name,
            "value": self.value
        }

    @override
    def to_compact_representation(self, indent: int) -> list[str]:
        return [f"{" " * indent}{self.value} matches 0xA2"]
