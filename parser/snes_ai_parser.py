from typing import override

from .abstract_ai_parser import AbstractAIParser
from .enums.game_version import GameVersion


class SNESAIParser(AbstractAIParser):
    def __init__(self) -> None:
        super().__init__(game_version=GameVersion.SNES, write_individual_ai_scripts=False)

    @override
    def load_config(self) -> dict[str, str]:
        return AbstractAIParser.load_and_normalise_config(bad_prefix="gba_", good_prefix="snes_")
