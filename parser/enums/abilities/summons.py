from enum import IntEnum
from typing import override


class Summons(IntEnum):
    CHOCOBO = 0x48
    SYLPH = 0x49
    REMORA = 0x4A
    SHIVA = 0x4B
    RAMUH = 0x4C
    IFRIT = 0x4D
    TITAN = 0x4E
    GOLEM = 0x4F
    CATOBLEPAS = 0x50
    CARBUNCLE = 0x51
    SYLDRA = 0x52
    ODIN = 0x53
    PHOENIX = 0x54
    LEVIATHAN = 0x55
    BAHAMUT = 0x56
    CHOCO_KICK = 0x5F
    WHISPERWIND = 0x60
    CONSTRICT = 0x61
    DIAMOND_DUST = 0x62
    JUDGMENT_BOLT = 0x63
    HELLFIRE = 0x64
    GAIA_S_WRATH = 0x65
    EARTHEN_WALL = 0x66
    DEMON_EYE = 0x67
    RUBY_LIGHT = 0x68
    THUNDERSTORM = 0x69
    ZANTETSUKEN = 0x6A
    FLAMES_OF_REBIRTH_DAMAGE = 0x6B
    TSUNAMI = 0x6C
    MEGA_FLARE = 0x6D
    FAT_CHOCOBO = 0x6E
    GUNGNIR = 0x6F
    FLAMES_OF_REBIRTH_RESURRECTION = 0x70
    EGG_CHOP = 0x73

    @override
    def __str__(self) -> str:
        if 0x48 <= self.value <= 0x56:
            return f"{self.name.title()} (summon)"
        elif self in (Summons.FLAMES_OF_REBIRTH_DAMAGE, Summons.FLAMES_OF_REBIRTH_RESURRECTION):
            return f"Flames of Rebirth ({"damage" if self == Summons.FLAMES_OF_REBIRTH_DAMAGE else "resurrection"})"
        else:
            return self.name.replace("_", " ").title().replace(" S ", "'s ")

    @classmethod
    def is_valid_id(cls, value: int) -> bool:
        return value in cls._value2member_map_
