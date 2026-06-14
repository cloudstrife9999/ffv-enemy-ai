from __future__ import annotations
from enum import IntEnum
from typing import override, Optional


class MatchType(IntEnum):
    MATCH = 0x00
    NO_MATCH = 0x01   # representative value

    @classmethod
    def _missing_(cls, value: object) -> Optional[MatchType]:
        if isinstance(value, int) and 0x00 <= value <= 0xFF:
            return cls.NO_MATCH
        else:
            raise ValueError(f"{value} is not a valid {cls.__name__}")

    @override
    def __str__(self) -> str:
        match self:
            case MatchType.MATCH:
                return "All parameters match"
            case MatchType.NO_MATCH:
                return "At least one parameter does not match"
            case _:
                raise ValueError(f"{self} is not a valid {self.__class__.__name__}.")
