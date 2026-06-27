from typing import Any, override

from .action import AIRuleAction
from ..enums.action_code import ActionCode
from ..enums.visual_and_sound_effect import VisualAndSoundEffect
from ..enums.visual_and_sound_effect_table import VisualAndSoundEffectTable


class VisualOrSoundEffectAction(AIRuleAction):
    def __init__(self, table_id: int, effect_id: int) -> None:
        super().__init__(action_code=ActionCode.VISUAL_OR_SOUND_EFFECT, optional_second_byte=table_id, optional_third_byte=effect_id, optional_fourth_byte=None)

    @property
    def table_id(self) -> VisualAndSoundEffectTable:
        if self.raw_second_byte is None:
            raise ValueError("Second byte is not set.")
        else:
            return VisualAndSoundEffectTable(self.raw_second_byte)

    @property
    def effect_id(self) -> VisualAndSoundEffect:
        if self.raw_third_byte is None:
            raise ValueError("Third byte is not set.")
        else:
            return VisualAndSoundEffect.from_table_and_effect_id(self.table_id, self.raw_third_byte)

    @override
    def terminates_turn_by_default(self) -> bool:
        return False

    @override
    def to_json(self) -> str | dict[str, Any]:
        return {
            "action": str(self.action_code),
            "effect_type": str(self.table_id),
            "effect": str(self.effect_id)
        }

    @override
    def to_compact_representation(self, indent: int) -> list[str]:
        return [f"{" " * indent}{str(self.effect_id)}"]
