from enum import IntEnum
from typing import override


class Special(IntEnum):
    CRITICAL_ATTACK = 0x00
    NEEDLE = 0x01
    INCISOR = 0x02
    TAIL = 0x03
    CLAW = 0x04
    PINCER = 0x05
    MAGIC_STICK = 0x06
    EIGHT_ARMS = 0x07
    TEN_ARMS = 0x08
    HORN = 0x09
    RUSH = 0x0A
    BODY_SLAM = 0x0B
    TURTLE = 0x0C
    DIVE = 0x0D
    FIN = 0x0E
    FEELER = 0x0F
    LICK = 0x10
    BITE = 0x11
    ELBOW = 0x12
    AXE = 0x13
    HEADBUTT = 0x14
    RIGHT_CLAW = 0x15
    TACKLE = 0x16
    SLAP = 0x17
    SPEAR = 0x18
    WING_ATTACK = 0x19
    THRUST = 0x1A
    FLYING_KNEE = 0x1B
    SPIRIT_BLAST = 0x1C
    TUSK = 0x1D
    UNUSED_INVISIBLE_FIST = 0x1E
    PUNCTURE = 0x1F
    LEFT_JAB = 0x20
    SLING = 0x21
    TOE_KICK = 0x22
    MINEUCHI = 0x23
    PRESSURE = 0x24
    HOSE = 0x25
    AIR_FIST = 0x26
    HIGH_KICK = 0x27
    CRUSH = 0x28
    KNOCK_SILLY = 0x29
    SQUEEZE = 0x2A
    DRILL = 0x2B
    WRING = 0x2C
    SICKLE = 0x2D
    YAGYUU_S_STRIKE = 0x2E
    CAT_SCRATCH = 0x2F
    CORNER = 0x30
    VENOMOUS_CLASP = 0x31
    TAKEDOWN = 0x32
    SAP = 0x33
    RAY = 0x34
    COUNTER = 0x35
    VACUUM_WAVE = 0x36
    KNIFE = 0x37 #
    VACUUM_WAVE_2 = 0x38  # Exclusive to Neo Exdeath's back part, Enuo (1st form, right hand, and left hand), and Necrophobia (Cloister of the Dead).
    DIMENSION_ZERO = 0x39
    UNUSED_0X3A = 0x3A
    SILVER_POWDER = 0x3B
    POISON_POWDER = 0x3C
    DARKNESS_POWDER = 0x3D
    PARALYZE_POWDER = 0x3E
    CONFUSE_POWDER = 0x3F

    @override
    def __str__(self) -> str:
        match self:
            case Special.UNUSED_0X3A:
                return "Unused 0x3A"
            case _:
                return self.name.replace("_", " ").title().replace(" S ", "'s ")

    @classmethod
    def is_valid_id(cls, value: int) -> bool:
        return value in cls._value2member_map_
