from enum import IntEnum
from typing import override


class TimeMagic(IntEnum):
    SPEED = 0x36
    SLOW = 0x37
    REGEN = 0x38
    MUTE = 0x39
    HASTE = 0x3A
    FLOAT = 0x3B
    GRAVITY = 0x3C
    STOP = 0x3D
    TELEPORT = 0x3E
    COMET = 0x3F
    SLOWGA = 0x40
    RETURN = 0x41
    GRAVIGA = 0x42
    HASTEGA = 0x43
    OLD = 0x44
    METEOR = 0x45
    QUICK = 0x46
    BANISH = 0x47

    @override
    def __str__(self) -> str:
        return self.name.title()

    @classmethod
    def is_valid_id(cls, value: int) -> bool:
        return value in cls._value2member_map_
