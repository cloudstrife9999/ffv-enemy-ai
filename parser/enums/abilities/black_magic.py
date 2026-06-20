from enum import IntEnum
from typing import override


class BlackMagic(IntEnum):
    FIRE = 0x24
    BLIZZARD = 0x25
    THUNDER = 0x26
    POISON = 0x27
    SLEEP = 0x28
    TOAD = 0x29
    FIRA = 0x2A
    BLIZZARA = 0x2B
    THUNDARA = 0x2C
    DRAIN = 0x2D
    BREAK = 0x2E
    BIO = 0x2F
    FIRAGA = 0x30
    BLIZZAGA = 0x31
    THUNDAGA = 0x32
    FLARE = 0x33
    DEATH = 0x34
    OSMOSE = 0x35
    
    @override
    def __str__(self) -> str:
        return self.name.title()

    @classmethod
    def is_valid_id(cls, value: int) -> bool:
        return value in cls._value2member_map_
