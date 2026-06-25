from enum import IntEnum
from typing import override


class SNESStatsAndPropertiesTable(IntEnum):
    STATUS_1 = 0x1A
    STATUS_2 = 0x1B
    STATUS_3 = 0x1C
    STATUS_4 = 0x1D
    ACTION_FLAGS = 0x1E  # the ActionFlags enum is used to interpret the value at this offset.

    @override
    def __str__(self) -> str:
        match self:
            case SNESStatsAndPropertiesTable.STATUS_1:
                return "Status table #1"
            case SNESStatsAndPropertiesTable.STATUS_2:
                return "Status table #2"
            case SNESStatsAndPropertiesTable.STATUS_3:
                return "Status table #3"
            case SNESStatsAndPropertiesTable.STATUS_4:
                return "Status table #4"
            case SNESStatsAndPropertiesTable.ACTION_FLAGS:
                return "Action flags"
            case _:
                raise ValueError(f"Unknown enum member: {self}.")

    @classmethod
    def is_valid_party_member_property_offset(cls, value: int) -> bool:
        return value in cls._value2member_map_
