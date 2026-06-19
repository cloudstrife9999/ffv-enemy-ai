from __future__ import annotations
from enum import Enum
from typing import override

from .global_event_table import GlobalEventTable


class GlobalEvent(Enum):
    RAMUH_DEFEATED = (GlobalEventTable.FIRST, 0x80)
    CATOBLEPAS_DEFEATED = (GlobalEventTable.FIRST, 0x40)
    GOLEM_BONE_DRAGON_ZOMBIE_DRAGON_DEFEATED = (GlobalEventTable.FIRST, 0x20)
    SOLO_GOLEM_BATTLE_UNAVAILABLE = (GlobalEventTable.FIRST, 0x10)
    SEKHMET_DEFEATED = (GlobalEventTable.FIRST, 0x08)
    GILGAMESH_AVAILABLE_IN_THE_INTERDIMENSIONAL_RIFT = (GlobalEventTable.FIRST, 0x04)
    KING_BEHEMOTH_DEFEATED = (GlobalEventTable.FIRST, 0x02)
    UNKNOWN_0101_FLAG = (GlobalEventTable.FIRST, 0x01)
    GALUF_SOLO_VS_EXDEATH_ALREADY_HAPPENED = (GlobalEventTable.SECOND, 0x80)
    UNKNOWN_0240_FLAG = (GlobalEventTable.SECOND, 0x40)
    UNKNOWN_0220_FLAG = (GlobalEventTable.SECOND, 0x20)
    UNKNOWN_0210_FLAG = (GlobalEventTable.SECOND, 0x10)
    UNKNOWN_0208_FLAG = (GlobalEventTable.SECOND, 0x08)
    UNKNOWN_0204_FLAG = (GlobalEventTable.SECOND, 0x04)
    UNKNOWN_0202_FLAG = (GlobalEventTable.SECOND, 0x02)
    UNKNOWN_0201_FLAG = (GlobalEventTable.SECOND, 0x01)
    BARTZ_IS_IN_THE_PARTY = (GlobalEventTable.THIRD, 0x80)
    LENNA_IS_IN_THE_PARTY = (GlobalEventTable.THIRD, 0x40)
    GALUF_IS_IN_THE_PARTY = (GlobalEventTable.THIRD, 0x20)
    FARIS_IS_IN_THE_PARTY = (GlobalEventTable.THIRD, 0x10)
    KRILE_IS_IN_THE_PARTY = (GlobalEventTable.THIRD, 0x08)
    UNKNOWN_0304_FLAG = (GlobalEventTable.THIRD, 0x04)
    UNKNOWN_0302_FLAG = (GlobalEventTable.THIRD, 0x02)
    UNKNOWN_0301_FLAG = (GlobalEventTable.THIRD, 0x01)
    UNKNOWN_0480_FLAG = (GlobalEventTable.FOURTH, 0x80)
    UNKNOWN_0440_FLAG = (GlobalEventTable.FOURTH, 0x40)
    UNKNOWN_0420_FLAG = (GlobalEventTable.FOURTH, 0x20)
    UNKNOWN_0410_FLAG = (GlobalEventTable.FOURTH, 0x10)
    UNKNOWN_0408_FLAG = (GlobalEventTable.FOURTH, 0x08)
    UNKNOWN_0404_FLAG = (GlobalEventTable.FOURTH, 0x04)
    UNKNOWN_0402_FLAG = (GlobalEventTable.FOURTH, 0x02)
    UNKNOWN_0401_FLAG = (GlobalEventTable.FOURTH, 0x01)

    def __init__(self, table: GlobalEventTable, mask: int) -> None:
        self.table: GlobalEventTable = table
        self.mask: int = mask

    @classmethod
    def from_table_and_mask(cls, table: GlobalEventTable, mask: int) -> list[GlobalEvent]:
        events: list[GlobalEvent] = []

        for status in cls:
            if status.table is table:
                # Basically, the mask can cover more than one event, so we need to check if the mask includes this event's mask.
                if status.mask & mask:
                    events.append(status)

        if events:
            return events
        else:
            raise ValueError(f"Invalid global event code: table={table}, mask={mask:#04x}")

    @override
    def __str__(self) -> str:
        return self.name.replace("_", " ").title()  # TODO: refine this.
