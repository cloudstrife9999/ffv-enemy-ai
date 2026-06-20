from enum import IntEnum
from typing import override


class Songs(IntEnum):
    SINEWY_ETUDE = 0x57
    SWIFT_SONG = 0x58
    MIGHTY_MARCH = 0x59
    MANA_S_PAEAN = 0x5A
    HERO_S_RIME = 0x5B
    REQUIEM = 0x5C
    ROMEO_S_BALLAD = 0x5D
    ALLURING_AIR = 0x5E

    @override
    def __str__(self) -> str:
        return self.name.replace("_", " ").title().replace(" S ", "'s ")

    @classmethod
    def is_valid_id(cls, value: int) -> bool:
        return value in cls._value2member_map_
