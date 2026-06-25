from enum import Enum
from typing import override


class GameVersion(Enum):
    SNES = "snes"
    GBA = "gba"

    @override
    def __str__(self) -> str:
        match self:
            case GameVersion.SNES:
                return "SNES"
            case GameVersion.GBA:
                return "Advance"
            case _:
                raise ValueError(f"Unknown game version: {self.value}")
