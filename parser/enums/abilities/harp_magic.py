from enum import IntEnum
from typing import override


class HarpMagic(IntEnum):
    SILVER_HARP = 0x74
    DREAM_HARP = 0x75
    LAMIA_S_HARP = 0x76
    APOLLO_S_HARP = 0x77
    
    @override
    def __str__(self) -> str:
        return f"{self.name.replace("_", " ").title().replace(" S ", "'s ")}'s spell"

    @classmethod
    def is_valid_id(cls, value: int) -> bool:
        return value in cls._value2member_map_
