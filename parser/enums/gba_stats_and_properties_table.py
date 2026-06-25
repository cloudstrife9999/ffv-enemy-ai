from enum import IntEnum
from typing import override


class GBAStatsAndPropertiesTable(IntEnum):
    STATUS_1 = 0x14
    STATUS_2 = 0x15
    STATUS_3 = 0x16
    STATUS_4 = 0x17
    CMD_STATUS = 0x18  # the CommandStatus enum is used to interpret the value at this offset.

    @override
    def __str__(self) -> str:
        return self.name.replace("_", " ").title()  # TODO: refine this.

    @classmethod
    def is_valid_party_member_property_offset(cls, value: int) -> bool:
        return value in cls._value2member_map_
