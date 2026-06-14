from __future__ import annotations
from enum import Enum
from typing import override


class Element(Enum):
    WATER = 0x80
    WIND = 0x40
    EARTH = 0x20
    HOLY = 0x10
    POISON = 0x08
    LIGHTNING = 0x04
    ICE = 0x02
    FIRE = 0x01

    @classmethod
    def from_mask(cls, mask: int) -> list[Element]:
        matching_elements: list[Element] = []

        for element in cls:
            if mask & element.value:
                matching_elements.append(element)

        return matching_elements

    @override
    def __str__(self) -> str:
        return self.name.title()
