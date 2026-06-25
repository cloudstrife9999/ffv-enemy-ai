from typing import Any, override

from .condition import AIRuleCondition
from ..enums.condition_code import ConditionCode
from ..enums.match import MatchType
from ..enums.enemy_slot import EnemySlot


class EnemySlotsCondition(AIRuleCondition):
    def __init__(self, match_type: MatchType, third_byte: int, mask: int) -> None:
        super().__init__(ConditionCode.ENEMY_SLOTS.value, match_type.value, third_byte, mask)

    @property
    def match_type(self) -> MatchType:
        '''
        For this condition:
        - 0x00: the active enemy slots match the mask.
        - 0x01: the active enemy slots do not match the mask.
        '''
        return MatchType(self.raw_second_byte)

    @property
    def third_byte(self) -> int:
        return self.raw_third_byte

    @property
    def mask(self) -> int:
        return self.raw_fourth_byte

    @property
    def enemy_slots(self) -> list[EnemySlot]:
        return EnemySlot.from_mask(self.mask)

    @override
    def to_json(self) -> str | dict[str, Any]:
        return {
            "condition": str(self.condition_code),
            "match_type": str(self.match_type),
            "explanation": "visible enemies only in these slots" if self.match_type == MatchType.MATCH else "either one of these slots is empty, or there is at least a visible enemy in a slot not in this list",
            "enemy_slots": [", ".join(f"#{slot.name.split("_")[1]}" for slot in self.enemy_slots)]
        }

    @override
    def to_compact_representation(self, indent: int) -> list[str]:
        if self.match_type == MatchType.MATCH:
            return [f"{" " * indent}No visible enemies in slots other than [{", ".join(f"#{slot.name.split("_")[1]}" for slot in self.enemy_slots)}]"]
        else:
            return [f"{" " * indent}At least one visible enemy in any of the following slots: [{", ".join(f"#{slot.name.split("_")[1]}" for slot in self.enemy_slots)}]"]
