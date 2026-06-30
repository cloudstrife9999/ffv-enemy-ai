from typing import Any, override

from .condition import AIRuleCondition
from ..enums.condition_code import ConditionCode
from ..enums.target_count import TargetCount


class TargetCountCondition(AIRuleCondition):
    def __init__(self, second_byte: int, third_byte: int, target_count: TargetCount) -> None:
        super().__init__(ConditionCode.TARGET_COUNT.value, second_byte, third_byte, target_count.value)

    @property
    def target_count(self) -> TargetCount:
        return TargetCount(self.raw_fourth_byte)

    @override
    def to_json(self) -> str | dict[str, Any]:
        return {
            "condition": str(self.condition_code),
            "target_count": str(self.target_count)
        }

    @override
    def to_compact_representation(self, indent: int) -> list[str]:
        return [f"{" " * indent}Hit by a {"single-target" if self.target_count == TargetCount.SINGLE else "multi-target"} action"]
