from typing import Any, override

from .condition import AIRuleCondition
from ..enums.condition_code import ConditionCode
from ..enums.target import Target


class HPThresholdCondition(AIRuleCondition):
    def __init__(self, target: Target, hp_threshold_lsb: int, hp_threshold_msb: int) -> None:
        super().__init__(ConditionCode.HP_LOWER_THAN_THRESHOLD.value, target.value, hp_threshold_lsb, hp_threshold_msb)

    @property
    def target(self) -> Target:
        return Target(self.raw_second_byte)

    @property
    def hp_threshold(self) -> int:
        return (self.raw_fourth_byte << 8) | self.raw_third_byte

    @override
    def to_json(self) -> str | dict[str, Any]:
        return {
            "condition": self.condition_code.name,
            "target": self.target.name,
            "hp_threshold": self.hp_threshold
        }
