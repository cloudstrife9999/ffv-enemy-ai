from typing import Any, override

from .condition import AIRuleCondition
from ..enums.condition_code import ConditionCode


class LoneEnemyCondition(AIRuleCondition):
    def __init__(self, collapse_duplicates_byte: int, third_byte: int, fourth_byte: int) -> None:
        '''
        Meaning of `collapse_duplicates_byte`:
        - 0  = duplicates of the same enemy count as separate enemies (e.g., if there are 2 of the same enemy, this condition will be false).
        - 1+ = duplicates of the same enemy do not count as separate enemies (e.g., if there are 2 of the same enemy, this condition will be true).
        '''
        super().__init__(ConditionCode.LONE_ENEMY.value, collapse_duplicates_byte, third_byte, fourth_byte)

    @override
    def to_json(self) -> str | dict[str, Any]:
        return {
            "condition": str(self.condition_code),
            "duplicates_count_as_separate_enemies": bool(not self.raw_second_byte)
        }

    @override
    def to_compact_representation(self, indent: int) -> list[str]:
        return [f"{" " * indent}{str(self.condition_code)} (duplicates{" " if self.raw_second_byte else " do not "}count as separate enemies)"]
