from typing import Any, override

from .action import AIRuleAction
from ..enums.action_code import ActionCode


class UnhideEnemyAction(AIRuleAction):
    def __init__(self, mask: int, enemy_set: int) -> None:
        super().__init__(action_code=ActionCode.UNHIDE_ENEMY, optional_second_byte=mask, optional_third_byte=enemy_set, optional_fourth_byte=None)

    @property
    def mask(self) -> int:
        if not self.raw_second_byte:
            raise ValueError("Mask is not set.")
        else:
            return self.raw_second_byte

    @property
    def enemy_set(self) -> int:
        if not self.raw_third_byte:
            raise ValueError("Enemy set is not set.")
        else:
            return self.raw_third_byte

    @override
    def to_json(self) -> str | dict[str, Any]:
        return {
            "action": self.action_code.name,
            "mask": self.mask,
            "enemy_set": self.enemy_set
        }
