from __future__ import annotations
from enum import Enum
from typing import override


class EnemySlot(Enum):
    SLOT_1 = 0x80
    SLOT_2 = 0x40
    SLOT_3 = 0x20
    SLOT_4 = 0x10
    SLOT_5 = 0x08
    SLOT_6 = 0x04
    SLOT_7 = 0x02
    SLOT_8 = 0x01

    @classmethod
    def from_mask(cls, mask: int) -> list[EnemySlot]:
        matching_slots: list[EnemySlot] = []

        for slot in cls:
            if mask & slot.value:
                matching_slots.append(slot)

        return matching_slots

    @override
    def __str__(self) -> str:
        return self.name.replace("_", " #").title()
