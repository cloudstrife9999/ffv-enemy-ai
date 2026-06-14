from enum import IntEnum
from typing import override


class SymbolCode(IntEnum):
    NO_INTERRUPT_PADDING = 0xF0
    SEPARATOR = 0xFE
    TERMINATOR = 0xFF

    @override
    def __str__(self) -> str:
        return self.name.title()
