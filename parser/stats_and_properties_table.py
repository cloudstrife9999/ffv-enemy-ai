from .enums.snes_stats_and_properties_table import SNESStatsAndPropertiesTable
from .enums.gba_stats_and_properties_table import GBAStatsAndPropertiesTable
from .enums.game_version import GameVersion


class StatsAndPropertiesTable():
    @staticmethod
    def is_valid_party_member_property_offset(game_version: GameVersion, offset: int) -> bool:
        match game_version:
            case GameVersion.SNES:
                return SNESStatsAndPropertiesTable.is_valid_party_member_property_offset(offset)
            case GameVersion.GBA:
                return GBAStatsAndPropertiesTable.is_valid_party_member_property_offset(offset)
            case _:
                raise ValueError(f"Unsupported game version: {game_version}.")
