from enum import IntEnum
from typing import override


class GlobalEventTable(IntEnum):
    FIRST = 0x00
    SECOND = 0x01
    THIRD = 0x02
    FOURTH = 0x03
    FIFTH = 0x04
    SIXTH = 0x05
    SEVENTH = 0x06
    EIGHTH = 0x07
    NINTH = 0x08
    TENTH = 0x09
    ELEVENTH = 0x0A
    TWELFTH = 0x0B
    THIRTEENTH = 0x0C
    FOURTEENTH = 0x0D
    FIFTEENTH = 0x0E

    @override
    def __str__(self) -> str:
        return f"{self.name.title()} table"
