from enum import IntEnum
from typing import override


class StatusTable(IntEnum):
    FIRST = 0x00
    SECOND = 0x01
    THIRD = 0x02
    FOURTH = 0x03

    @override
    def __str__(self) -> str:
        return f"{self.name.title()} table"
