from enum import IntEnum
from typing import override


class DarkArts(IntEnum):
    DRAIN_TOUCH = 0xF3
    DARK_HAZE = 0xF4
    DEEP_FREEZE = 0xF5
    EVIL_MIST = 0xF6
    MELTDOWN = 0xF7
    HELLWIND = 0xF8
    CHAOS_DRIVE = 0xF9
    CURSE = 0xFA
    DARK_FLARE = 0xFB
    DOOMSDAY = 0xFC

    @override
    def __str__(self) -> str:
        return self.name.replace("_", " ").title()

    @classmethod
    def is_valid_id(cls, value: int) -> bool:
        return value in cls._value2member_map_
