from typing import Any, override

from .action import AIRuleAction
from ..enums.ability import Ability
from ..enums.dark_arts import DarkArts


class SimpleAction(AIRuleAction):
    def __init__(self, action_code: int) -> None:
        super().__init__(action_code, optional_second_byte=None, optional_third_byte=None, optional_fourth_byte=None)

        if not (0x00 <= action_code <= 0xFC):
            raise ValueError(f"Invalid action code: {action_code:#04x}. It must be between 0x00 and 0xFC (inclusive).")

    @property
    def action(self) -> Ability | DarkArts:
        if Ability.is_valid_ability_id(self.raw_action_code):
            return Ability(self.raw_action_code)
        elif DarkArts.is_valid_ability_id(self.raw_action_code):
            return DarkArts(self.raw_action_code)
        else:
            raise ValueError(f"Invalid action code: {self.raw_action_code:#04x}")

    @override
    def terminates_turn_by_default(self) -> bool:
        return True

    @override
    def to_json(self) -> str | dict[str, Any]:
        return str(self.action)

    @override
    def to_compact_representation(self, indent: int) -> list[str]:
        if self.action is Ability.NOTHING:
            return [f"{" " * indent}Nothing"]
        else:
            return [f"{" " * indent}Ability: {str(self.action)}"]
