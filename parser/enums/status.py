from __future__ import annotations
from enum import Enum
from typing import override

from .status_table import StatusTable


class StatusCode(Enum):
    DEATH = StatusTable.FIRST, 0x80
    PETRIFY = StatusTable.FIRST, 0x40
    TOAD = StatusTable.FIRST, 0x20
    MINI = StatusTable.FIRST, 0x10
    FLOAT = StatusTable.FIRST, 0x08
    POISON = StatusTable.FIRST, 0x04
    ZOMBIE = StatusTable.FIRST, 0x02
    DARKNESS = StatusTable.FIRST, 0x01

    OLD = StatusTable.SECOND, 0x80
    SLEEP = StatusTable.SECOND, 0x40
    PARALYZE = StatusTable.SECOND, 0x20
    CONFUSE = StatusTable.SECOND, 0x10
    BERSERK = StatusTable.SECOND, 0x08
    SILENCE = StatusTable.SECOND, 0x04
    IMAGE_2 = StatusTable.SECOND, 0x02
    IMAGE_1 = StatusTable.SECOND, 0x01

    REFLECT = StatusTable.THIRD, 0x80
    PROTECT = StatusTable.THIRD, 0x40
    SHELL = StatusTable.THIRD, 0x20
    STOP = StatusTable.THIRD, 0x10
    HASTE = StatusTable.THIRD, 0x08
    SLOW = StatusTable.THIRD, 0x04
    INVINCIBLE = StatusTable.THIRD, 0x02
    REGEN = StatusTable.THIRD, 0x01

    ERASED = StatusTable.FOURTH, 0x80
    FALSE_IMAGE = StatusTable.FOURTH, 0x40
    CONTROLLED = StatusTable.FOURTH, 0x20
    DOOM = StatusTable.FOURTH, 0x10
    SAP = StatusTable.FOURTH, 0x08
    SINGING = StatusTable.FOURTH, 0x04
    CRITICAL = StatusTable.FOURTH, 0x02
    HIDDEN = StatusTable.FOURTH, 0x01

    def __init__(self, table: StatusTable, mask: int) -> None:
        self.table: StatusTable = table
        self.mask: int = mask

    @classmethod
    def from_table_and_mask(cls, table: StatusTable, mask: int) -> StatusCode:
        for status in cls:
            if status.table is table and status.mask == mask:
                return status

        raise ValueError(f"Invalid status code: table={table}, mask={mask:#04x}")

    @override
    def __str__(self) -> str:
        match self:
            case StatusCode.IMAGE_1 | StatusCode.IMAGE_2:
                return f"Image ({self.mask})"
            case _:
                return self.name.title().replace("_", " ")
