from enum import IntEnum
from typing import override


class Spellblade(IntEnum):
    FIRE = 0x00
    BLIZZARD = 0x01
    THUNDER = 0x02
    POISON = 0x03
    SILENCE = 0x04
    SLEEP = 0x05
    FIRA = 0x06
    BLIZZARA = 0x07
    THUNDARA = 0x08
    DRAIN = 0x09
    BREAK = 0x0A
    BIO = 0x0B
    FIRAGA = 0x0C
    BLIZZAGA = 0x0D
    THUNDAGA = 0x0E
    HOLY = 0x0F
    FLARE = 0x10
    OSMOSE = 0x11
    
    @override
    def __str__(self) -> str:
        return f"{self.name.title()} spellblade"

    @classmethod
    def is_valid_id(cls, value: int) -> bool:
        return value in cls._value2member_map_
