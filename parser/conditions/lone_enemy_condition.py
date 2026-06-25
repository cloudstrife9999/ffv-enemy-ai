from typing import Any, override

from .condition import AIRuleCondition
from ..enums.condition_code import ConditionCode


# TODO: the third byte is the count of enemies (other than this enemy) for this condition to be true.
class LoneEnemyCondition(AIRuleCondition):
    def __init__(self, second_byte: int, third_byte: int, fourth_byte: int) -> None:
        super().__init__(ConditionCode.LONE_ENEMY.value, second_byte, third_byte, fourth_byte)

    @override
    def to_json(self) -> str | dict[str, Any]:
        return str(self.condition_code)

    @override
    def to_compact_representation(self, indent: int) -> list[str]:
        return [f"{" " * indent}{str(self.condition_code)}"]
