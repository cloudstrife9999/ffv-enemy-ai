from enum import Enum
from typing import override


class ActionFlags(Enum):
    DEFENDING = 0x80
    GUARDING = 0x40
    UNKNOWN_20 = 0x20
    JUMPING = 0x10
    FLIRTING = 0x08
    UNKNOWN_04 = 0x04
    UNKNOWN_02 = 0x02
    UNKNOWN_01 = 0x01

    @override
    def __str__(self) -> str:
        match self:
            case ActionFlags.UNKNOWN_01 | ActionFlags.UNKNOWN_02 | ActionFlags.UNKNOWN_04 | ActionFlags.UNKNOWN_20:
                return f"Unknown (0x{self.value:02X})"
            case _:
                return self.name.title()
