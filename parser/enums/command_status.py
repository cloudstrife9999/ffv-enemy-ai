from enum import Enum
from typing import override


class CommandStatus(Enum):
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
            case CommandStatus.UNKNOWN_01 | CommandStatus.UNKNOWN_02 | CommandStatus.UNKNOWN_04 | CommandStatus.UNKNOWN_20:
                return f"Unknown ({self.value:#04x})"
            case _:
                return self.name.title()
