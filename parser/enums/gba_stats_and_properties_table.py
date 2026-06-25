from enum import IntEnum
from typing import override


class GBAStatsAndPropertiesTable(IntEnum):
    STATUS_1 = 0x14
    STATUS_2 = 0x15
    STATUS_3 = 0x16
    STATUS_4 = 0x17
    ACTION_FLAGS = 0x18  # the ActionFlags enum is used to interpret the value at this offset.

    @override
    def __str__(self) -> str:
        match self:
            case GBAStatsAndPropertiesTable.STATUS_1:
                return "Status table #1"
            case GBAStatsAndPropertiesTable.STATUS_2:
                return "Status table #2"
            case GBAStatsAndPropertiesTable.STATUS_3:
                return "Status table #3"
            case GBAStatsAndPropertiesTable.STATUS_4:
                return "Status table #4"
            case GBAStatsAndPropertiesTable.ACTION_FLAGS:
                return "Action flags"
            case _:
                raise ValueError(f"Unknown enum member: {self}.")

    @classmethod
    def is_valid_party_member_property_offset(cls, value: int) -> bool:
        return value in cls._value2member_map_
