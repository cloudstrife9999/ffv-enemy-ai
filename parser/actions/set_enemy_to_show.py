from typing import Any, override

from .action import AIRuleAction
from ..enums.action_code import ActionCode
from ..enums.enemy_slot import EnemySlot
from ..enums.transformation_flags import TransformationFlags


class SetEnemyToShowAction(AIRuleAction):
    def __init__(self, flags: int, slot_mask: int) -> None:
        super().__init__(action_code=ActionCode.SET_ENEMY_TO_SHOW, optional_second_byte=flags, optional_third_byte=slot_mask, optional_fourth_byte=None)

        self.__enemy_slots: list[EnemySlot] = EnemySlot.from_mask(slot_mask)
        self.__transformation_flags: list[TransformationFlags] = TransformationFlags.from_mask(flags)

    @property
    def flags(self) -> int:
        if self.raw_second_byte is None:
            raise ValueError("Flags are not set.")
        else:
            return self.raw_second_byte

    @property
    def slot_mask(self) -> int:
        if self.raw_third_byte is None:
            raise ValueError("Slot mask is not set.")
        else:
            return self.raw_third_byte

    @property
    def enemy_slots(self) -> list[EnemySlot]:
        return self.__enemy_slots

    @property
    def transformation_flags(self) -> list[TransformationFlags]:
        return self.__transformation_flags

    @override
    def terminates_turn_by_default(self) -> bool:
        return False

    @override
    def to_json(self) -> str | dict[str, Any]:
        return {
            "action": self.action_code.name,
            "slot_mask": f"{self.slot_mask:08b}",
            "flags": f"{self.flags:08b}"
        }

    @override
    def to_compact_representation(self, indent: int) -> list[str]:
        return [
            f"{" " * indent}Prepare to show/hide enemies:"
        ] + [
            f"{" " * (indent + 2)}Relevant enemy slots: [{", ".join(f"#{slot.name.split("_")[1]}" for slot in self.enemy_slots)}]"
        ] + [
            f"{" " * (indent + 2)}Behaviour:"
        ] + [
            f"{" " * (indent + 4)}- {str(flag)}" for flag in self.transformation_flags
        ]
