from __future__ import annotations
from enum import IntEnum
from typing import override


class SpecialAbilityFlags(IntEnum):
    AUTO_HIT_AND_DEFENCE_PIERCING = 0x80
    OLD = 0x40
    POISON = 0x20
    DARKNESS = 0x10
    PARALYZE = 0x08
    CONFUSE = 0x04
    SAP = 0x02
    A_PLUS_50_PERCENT = 0x01

    @override
    def __str__(self) -> str:
        match self:
            case SpecialAbilityFlags.AUTO_HIT_AND_DEFENCE_PIERCING:
                return "Auto-hit and D = 0"
            case SpecialAbilityFlags.OLD:
                return "Old status"
            case SpecialAbilityFlags.POISON:
                return "Poison status"
            case SpecialAbilityFlags.DARKNESS:
                return "Darkness status"
            case SpecialAbilityFlags.PARALYZE:
                return "Paralyze status"
            case SpecialAbilityFlags.CONFUSE:
                return "Confuse status"
            case SpecialAbilityFlags.SAP:
                return "Sap status"
            case SpecialAbilityFlags.A_PLUS_50_PERCENT:
                return "Modifier: A = A + A//2"
            case _:
                raise ValueError(f"Unknown SpecialAbilityFlags value: {self.value}.")

    @staticmethod
    def from_bitmask(bitmask: int) -> list[SpecialAbilityFlags]:
        flags: list[SpecialAbilityFlags] = []

        for flag in SpecialAbilityFlags:
            if bitmask & flag.value:
                flags.append(flag)

        return flags

    @classmethod
    def is_valid_id(cls, value: int) -> bool:
        return value in cls._value2member_map_
