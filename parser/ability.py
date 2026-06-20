from typing import Union, TypeAlias

from .enums.abilities.black_magic import BlackMagic
from .enums.abilities.blue_magic import BlueMagic
from .enums.abilities.dance import Dance
from .enums.abilities.dark_arts import DarkArts
from .enums.abilities.enemy_abilities import EnemyAbilities
from .enums.abilities.other import OtherAbilities
from .enums.abilities.songs import Songs
from .enums.abilities.spellblade import Spellblade
from .enums.abilities.summons import Summons
from .enums.abilities.time_magic import TimeMagic
from .enums.abilities.white_magic import WhiteMagic


GenericAbility: TypeAlias = Union[BlackMagic, BlueMagic, Dance, DarkArts, EnemyAbilities, OtherAbilities, Songs, Spellblade, Summons, TimeMagic, WhiteMagic]


class Ability():
    @staticmethod
    def from_id(value: int) -> GenericAbility:
        if BlackMagic.is_valid_id(value):
            return BlackMagic(value)
        elif BlueMagic.is_valid_id(value):
            return BlueMagic(value)
        elif Dance.is_valid_id(value):
            return Dance(value)
        elif DarkArts.is_valid_id(value):
            return DarkArts(value)
        elif EnemyAbilities.is_valid_id(value):
            return EnemyAbilities(value)
        elif OtherAbilities.is_valid_id(value):
            return OtherAbilities(value)
        elif Songs.is_valid_id(value):
            return Songs(value)
        elif Spellblade.is_valid_id(value):
            return Spellblade(value)
        elif Summons.is_valid_id(value):
            return Summons(value)
        elif TimeMagic.is_valid_id(value):
            return TimeMagic(value)
        elif WhiteMagic.is_valid_id(value):
            return WhiteMagic(value)
        else:
            raise ValueError(f"Invalid ability ID: {value:#04x}")

    @staticmethod
    def is_valid_id(value: int) -> bool:
        return BlackMagic.is_valid_id(value) or \
               BlueMagic.is_valid_id(value) or \
               Dance.is_valid_id(value) or \
               DarkArts.is_valid_id(value) or \
               EnemyAbilities.is_valid_id(value) or \
               OtherAbilities.is_valid_id(value) or \
               Songs.is_valid_id(value) or \
               Spellblade.is_valid_id(value) or \
               Summons.is_valid_id(value) or \
               TimeMagic.is_valid_id(value) or \
               WhiteMagic.is_valid_id(value)

    @staticmethod
    def is_valid_non_dark_arts_id(value: int) -> bool:
        return BlackMagic.is_valid_id(value) or \
               BlueMagic.is_valid_id(value) or \
               Dance.is_valid_id(value) or \
               EnemyAbilities.is_valid_id(value) or \
               OtherAbilities.is_valid_id(value) or \
               Songs.is_valid_id(value) or \
               Spellblade.is_valid_id(value) or \
               Summons.is_valid_id(value) or \
               TimeMagic.is_valid_id(value) or \
               WhiteMagic.is_valid_id(value)
