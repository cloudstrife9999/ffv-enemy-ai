from __future__ import annotations
from enum import IntEnum
from typing import override, Optional


# TODO: check if it is more fine-grained than the current representation.
class TargetCount(IntEnum):
    SINGLE = 0x00
    MULTI = 0x01   # representative value

    @classmethod
    def _missing_(cls, value: object) -> Optional[TargetCount]:
        if isinstance(value, int) and 0x00 <= value <= 0xFF:
            return cls.MULTI
        else:
            raise ValueError(f"{value} is not a valid {cls.__name__}")

    @override
    def __str__(self) -> str:
        match self:
            case TargetCount.SINGLE:
                return "Single-target action"
            case TargetCount.MULTI:
                return "Multi-target action"
            case _:
                raise ValueError(f"{self} is not a valid {self.__class__.__name__}.")
