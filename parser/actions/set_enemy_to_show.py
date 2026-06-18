from typing import Any, override

from .action import AIRuleAction
from ..enums.action_code import ActionCode


class SetEnemyToShowAction(AIRuleAction):
    def __init__(self, slot_mask: int, enemy_formation_number: int) -> None:
        super().__init__(action_code=ActionCode.SET_ENEMY_TO_SHOW, optional_second_byte=slot_mask, optional_third_byte=enemy_formation_number, optional_fourth_byte=None)

    @property
    def slot_mask(self) -> int:
        if self.raw_second_byte is None:
            raise ValueError("Slot mask is not set.")
        else:
            return self.raw_second_byte

    @property
    def enemy_formation_number(self) -> int:
        if self.raw_third_byte is None:
            raise ValueError("Enemy formation number is not set.")
        else:
            return self.raw_third_byte

    @override
    def to_json(self) -> str | dict[str, Any]:
        return {
            "action": self.action_code.name,
            "slot_mask": f"{self.slot_mask:08b}",
            "enemy_formation_number": self.enemy_formation_number
        }

    @override
    def to_compact_representation(self, indent: int) -> list[str]:
        return [f"{" " * indent}Mark the enemy/enemies from formation {self.enemy_formation_number} to be shown according to slot mask {self.slot_mask:08b}"]
