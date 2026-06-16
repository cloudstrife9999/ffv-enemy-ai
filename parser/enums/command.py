from enum import IntEnum
from typing import override

class Command(IntEnum):
    OTHER = 0x00
    ITEMS = 0x01
    ROW = 0x02
    DEFEND = 0x03
    ATTACK = 0x04
    GUARD = 0x05
    KICK = 0x06
    ANY_COMMAND = 0x07
    CHAKRA = 0x08
    FLEE = 0x09
    STEAL = 0x0A
    MUG = 0x0B
    JUMP = 0x0C
    LANCE = 0x0D
    SMOKE = 0x0E
    IMAGE = 0x0F
    THROW = 0x10
    MINEUCHI = 0x11
    ZENINAGE = 0x12
    IAINUKI = 0x13
    ANIMALS = 0x14
    AIM = 0x15
    RAPID_FIRE = 0x16
    CALL = 0x17
    CHECK = 0x18
    SCAN = 0x19
    CALM = 0x1A
    CONTROL = 0x1B
    CATCH = 0x1C
    RELEASE = 0x1D
    MIX = 0x1E
    DRINK = 0x1F
    PRAY = 0x20
    REVIVE = 0x21
    GAIA = 0x22
    DUMMIED_0X23 = 0x23
    HIDE = 0x24
    SHOW = 0x25
    DUMMIED_0X26 = 0x26
    SING = 0x27
    FLIRT = 0x28
    DANCE = 0x29
    MIMIC = 0x2A
    ANY_SPELL = 0x2B

    @override
    def __str__(self) -> str:
        match self:
            case Command.OTHER | Command.ANY_COMMAND | Command.DUMMIED_0X23 | Command.DUMMIED_0X26 | Command.ANY_SPELL:
                return self.name.replace("_", " ").title()
            case _:
                return f"!{self.name.replace('_', ' ').title()}"

    @classmethod
    def is_valid_command_id(cls, value: int) -> bool:
        return value in cls._value2member_map_
