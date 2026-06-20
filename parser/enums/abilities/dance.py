from enum import IntEnum
from typing import override


class Dance(IntEnum):
    MYSTERY_WALTZ = 0x79
    JITTERBUG_DUET = 0x7A
    TEMPTING_TANGO = 0x7B
    SWORD_DANCE = 0x7D

    @override
    def __str__(self) -> str:
        return self.name.replace("_", " ").title()

    @classmethod
    def is_valid_id(cls, value: int) -> bool:
        return value in cls._value2member_map_
