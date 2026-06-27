from __future__ import annotations
from enum import Enum
from typing import override

from .visual_and_sound_effect_table import VisualAndSoundEffectTable


class VisualAndSoundEffect(Enum):
    BGM_THE_FIERCE_BATTLE = VisualAndSoundEffectTable.CHANGE_MUSIC, 0x01
    BGM_BATTLE_WITH_GILGAMESH = VisualAndSoundEffectTable.CHANGE_MUSIC, 0x22
    BGM_THE_EVIL_LORD_EXDEATH = VisualAndSoundEffectTable.CHANGE_MUSIC, 0x2D
    BGM_TREE_EXDEATH_DEFEATED = VisualAndSoundEffectTable.CHANGE_MUSIC, 0x3E
    LIGHT_FLASH = VisualAndSoundEffectTable.LIGHT_EFFECT, 0xF0
    SCREEN_SHAKE_ON = VisualAndSoundEffectTable.SHAKING_EFFECT, 0x04  # Pre-Almagest
    SCREEN_SHAKE_OFF = VisualAndSoundEffectTable.SHAKING_EFFECT, 0x84
    MULTICOLOUR_ON = VisualAndSoundEffectTable.BRIGHTNESS_EFFECT, 0x03  # Pre-`Grand Cross`
    MULTICOLOUR_OFF = VisualAndSoundEffectTable.BRIGHTNESS_EFFECT, 0x83

    def __init__(self, table: VisualAndSoundEffectTable, effect_id: int) -> None:
        self.table: VisualAndSoundEffectTable = table
        self.effect_id: int = effect_id

    @classmethod
    def from_table_and_effect_id(cls, table: VisualAndSoundEffectTable, effect_id: int) -> VisualAndSoundEffect:
        for effect in cls:
            if effect.table is table and effect.effect_id == effect_id:
                return effect

        raise ValueError(f"Invalid status code: table={table}, mask={effect_id:02X}.")

    @override
    def __str__(self) -> str:
        match self.table:
            case VisualAndSoundEffectTable.CHANGE_MUSIC:
                return f"Change music to \"{self.name.replace("BGM_", "").replace("_", " ").title()}\""
            case VisualAndSoundEffectTable.PLAY_SOUND_EFFECT:
                return f"Play sound effect: {self.name.replace("_", " ").title()}"
            case VisualAndSoundEffectTable.LIGHT_EFFECT:
                return f"Light effect: {self.name.replace("_", " ").title()}"
            case VisualAndSoundEffectTable.SHAKING_EFFECT:
                return f"Full screen effect: {self.name.replace("_", " ").title()}"
            case VisualAndSoundEffectTable.BRIGHTNESS_EFFECT:
                return f"Colour effect: {self.name.replace("_", " ").title()}"
            case VisualAndSoundEffectTable.VISUAL_EFFECTS:
                return f"Visual effect: {self.name.replace("_", " ").title()}"
            case _:
                raise ValueError(f"Invalid table ID: {self.table}.")
