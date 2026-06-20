from enum import IntEnum
from typing import override


class WhiteMagic(IntEnum):
    CURE = 0x12
    LIBRA = 0x13
    POISONA = 0x14
    SILENCE = 0x15
    PROTECT = 0x16
    MINI = 0x17
    CURA = 0x18
    RAISE = 0x19
    CONFUSE = 0x1A
    BLINK = 0x1B
    SHELL = 0x1C
    ESUNA = 0x1D
    CURAGA = 0x1E
    REFLECT = 0x1F
    BERSERK = 0x20
    ARISE = 0x21
    HOLY = 0x22
    DISPEL = 0x23

    @override
    def __str__(self) -> str:
        return self.name.title()

    @classmethod
    def is_valid_id(cls, value: int) -> bool:
        return value in cls._value2member_map_
