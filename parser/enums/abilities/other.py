from enum import IntEnum
from typing import override


class OtherAbilities(IntEnum):
    LANCE_HP_DRAIN = 0x71
    LANCE_MP_DRAIN = 0x72
    ITEM_FAIL = 0x78
    MAGIC_SHELL = 0x7C
    COMMAND_ICE_AURA_DUMMIED = 0x7E
    COMMAND_ENTANGLE_WHIP_MAGIC = 0x7F

    @override
    def __str__(self) -> str:
        match self:
            case OtherAbilities.LANCE_HP_DRAIN:
                return "!Lance (HP drain effect)"
            case OtherAbilities.LANCE_MP_DRAIN:
                return "!Lance (MP drain effect)"
            case OtherAbilities.ITEM_FAIL:
                return "Item Fail"
            case OtherAbilities.MAGIC_SHELL:
                return "Magic Shell"
            case OtherAbilities.COMMAND_ICE_AURA_DUMMIED:
                return "Ice Aura (Dummied)"
            case OtherAbilities.COMMAND_ENTANGLE_WHIP_MAGIC:
                return "Entangle (Whip Magic)"
            case _:
                raise ValueError(f"Unknown OtherAbilities value: {self.value}.")

    @classmethod
    def is_valid_id(cls, value: int) -> bool:
        return value in cls._value2member_map_
