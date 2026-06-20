from enum import IntEnum
from typing import override


class BlueMagic(IntEnum):
    DOOM = 0x82
    ROULETTE = 0x83
    AQUA_BREATH = 0x84
    LEVEL_5_DEATH = 0x85
    LEVEL_4_GRAVIGA = 0x86
    LEVEL_2_OLD = 0x87
    LEVEL_3_FLARE = 0x88
    POND_S_CHORUS = 0x89
    LILLIPUTIAN_LYRIC = 0x8A
    FLASH = 0x8B
    TIME_SLIP = 0x8C
    MOON_FLUTE = 0x8D
    DEATH_CLAW = 0x8E
    AERO = 0x8F
    AERA = 0x90
    AEROGA = 0x91
    FLAME_THROWER = 0x92
    GOBLIN_PUNCH = 0x93
    DARK_SPARK = 0x94
    OFF_GUARD = 0x95
    TRANSFUSION = 0x96
    MIND_BLAST = 0x97
    VAMPIRE = 0x98
    MAGIC_HAMMER = 0x99
    MIGHTY_GUARD = 0x9A
    SELF_DESTRUCT = 0x9B
    QUESTION_MARKS = 0x9C
    THOUSAND_NEEDLES = 0x9D
    WHITE_WIND = 0x9E
    MISSILE = 0x9F

    @override
    def __str__(self) -> str:
        match self:
            case BlueMagic.OFF_GUARD | BlueMagic.SELF_DESTRUCT:
                return self.name.replace("_", " ").title().replace(" ", "-")
            case BlueMagic.QUESTION_MARKS:
                return "????"
            case BlueMagic.THOUSAND_NEEDLES:
                return "1000 Needles"
            case _:
                return self.name.replace("_", " ").title()

    @classmethod
    def is_valid_id(cls, value: int) -> bool:
        return value in cls._value2member_map_
