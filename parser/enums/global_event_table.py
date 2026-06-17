from enum import IntEnum
from typing import override


class GlobalEventTable(IntEnum):
    FIRST = 0x01
    SECOND = 0x02
    THIRD = 0x03
    FOURTH = 0x04
    FIFTH = 0x05
    SIXTH = 0x06
    SEVENTH = 0x07
    EIGHTH = 0x08
    NINTH = 0x09
    TENTH = 0x0A
    ELEVENTH = 0x0B
    TWELFTH = 0x0C
    THIRTEENTH = 0x0D
    FOURTEENTH = 0x0E
    FIFTEENTH = 0x0F

    @override
    def __str__(self) -> str:
        return f"{self.name.title()} table"

    @classmethod
    def is_valid_global_event_table_id(cls, value: int) -> bool:
        return value in cls._value2member_map_
