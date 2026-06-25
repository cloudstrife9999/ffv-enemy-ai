from typing import Any, override

from .action import AIRuleAction
from ..ability import Ability, GenericAbility
from ..enums.abilities.dark_arts import DarkArts
from ..enums.abilities.enemy_abilities import EnemyAbilities


class SimpleAction(AIRuleAction):
    def __init__(self, action_code: int, enemy_special_ability: str) -> None:
        super().__init__(action_code,  optional_second_byte=None, optional_third_byte=None, optional_fourth_byte=None)

        self.__enemy_special_ability: str = enemy_special_ability

        if not (0x00 <= action_code <= 0xFC):
            raise ValueError(f"Invalid action code: {action_code:#04x}. It must be between 0x00 and 0xFC (inclusive).")

    @property
    def action(self) -> GenericAbility:
        if Ability.is_valid_id(self.raw_action_code):
            return Ability.from_id(self.raw_action_code)
        elif DarkArts.is_valid_id(self.raw_action_code):
            return DarkArts(self.raw_action_code)
        else:
            raise ValueError(f"Invalid action code: {self.raw_action_code:#04x}")

    @override
    def terminates_turn_by_default(self) -> bool:
        return True

    @override
    def to_json(self) -> str | dict[str, Any]:
        if self.action is EnemyAbilities.UNNAMED_STAY_IDLE:
            return "Stay idle"
        elif self.action is EnemyAbilities.UNNAMED_SPECIAL_ABILITY:
            return f"Special: {self.__enemy_special_ability}"
        else:
            return f"Ability: {str(self.action)}"

    @override
    def to_compact_representation(self, indent: int) -> list[str]:
        if self.action is EnemyAbilities.UNNAMED_STAY_IDLE:
            return [f"{" " * indent}{str(self.action)}"]
        elif self.action is EnemyAbilities.UNNAMED_SPECIAL_ABILITY:
            return [f"{" " * indent}Special: {self.__enemy_special_ability}"]
        else:
            return [f"{" " * indent}Ability: {str(self.action)}"]
