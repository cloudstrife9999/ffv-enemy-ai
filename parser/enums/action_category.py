from __future__ import annotations
from enum import Enum
from typing import override


class ActionCategory(Enum):
    PHYSICAL = 0x80
    AERIAL = 0x40
    SONG = 0x20
    SUMMON = 0x10
    TIME = 0x08
    BLACK = 0x04
    WHITE = 0x02
    BLUE = 0x01

    @classmethod
    def from_mask(cls, mask: int) -> list[ActionCategory]:
        matching_categories: list[ActionCategory] = []

        for element in cls:
            if mask & element.value:
                matching_categories.append(element)

        return matching_categories

    @override
    def __str__(self) -> str:
        return self.name.title()
