from enum import IntEnum
from typing import override


class ConditionCode(IntEnum):
    UNCONDITIONAL = 0x00
    STATUS_EFFECT = 0x01
    HP_LOWER_THAN_THRESHOLD = 0x02
    VAR_CHECK = 0x03
    LONE_ENEMY = 0x04
    ENEMY_SLOTS = 0x05
    HIT_BY_COMMAND_WITH_ELEMENT = 0x06
    HIT_BY_COMMAND_WITH_CATEGORY = 0x07
    HIT_BY_SPELL = 0x08
    HIT_BY_ITEM = 0x09
    TARGET_COUNT = 0x0A
    PARTY_MEMBER_PARAMETER = 0x0B
    COMPARE_WITH_A2 = 0x0C
    GLOBAL_EVENT_FLAGS = 0x0D
    HP_DAMAGE_JUST_TAKEN = 0x0E
    DEATH_COUNTER = 0x0F
    SINGLE_PARTY_MEMBER_ALIVE = 0x10
    HIT_BY_SUMMON = 0x11
    NO_FEMALE_PARTY_MEMBERS_TARGETABLE = 0x12

    @override
    def __str__(self) -> str:
        match self:
            case ConditionCode.UNCONDITIONAL:
                return "Unconditional"
            case ConditionCode.STATUS_EFFECT:
                return "Status effect"
            case ConditionCode.HP_LOWER_THAN_THRESHOLD:
                return "HP lower than threshold"
            case ConditionCode.VAR_CHECK:
                return "Variable check"
            case ConditionCode.LONE_ENEMY:
                return "Lone enemy"
            case ConditionCode.ENEMY_SLOTS:
                return "Enemy slots"
            case ConditionCode.HIT_BY_COMMAND_WITH_ELEMENT:
                return "Hit by command (belonging to zero or more elements)"
            case ConditionCode.HIT_BY_COMMAND_WITH_CATEGORY:
                return "Hit by command (belonging to one or more categories)"
            case ConditionCode.HIT_BY_SPELL:
                return "Hit by ability"
            case ConditionCode.HIT_BY_ITEM:
                return "Hit by item"
            case ConditionCode.TARGET_COUNT:
                return "Target count"
            case ConditionCode.PARTY_MEMBER_PARAMETER:
                return "Party member parameter"
            case ConditionCode.COMPARE_WITH_A2:
                return "Compare with A2"
            case ConditionCode.GLOBAL_EVENT_FLAGS:
                return "Global event flags"
            case ConditionCode.HP_DAMAGE_JUST_TAKEN:
                return "HP damage just taken"
            case ConditionCode.DEATH_COUNTER:
                return "Death counter"
            case ConditionCode.SINGLE_PARTY_MEMBER_ALIVE:
                return "Single party member alive"
            case ConditionCode.HIT_BY_SUMMON:
                return "Hit by summon"
            case ConditionCode.NO_FEMALE_PARTY_MEMBERS_TARGETABLE:
                return "No female party members targetable"
            case _:
                raise ValueError(f"{self} is not a valid {self.__class__.__name__}.")

    @classmethod
    def is_valid_condition_code(cls, value: int) -> bool:
        return value in cls._value2member_map_

    def has_irrelevant_second_byte(self) -> bool:
        '''Irrelevant as in "ignored by the game".'''
        return self in {
            ConditionCode.UNCONDITIONAL,
            ConditionCode.VAR_CHECK,
            ConditionCode.LONE_ENEMY,
            ConditionCode.COMPARE_WITH_A2,
            ConditionCode.GLOBAL_EVENT_FLAGS,
            ConditionCode.HP_DAMAGE_JUST_TAKEN,
            ConditionCode.DEATH_COUNTER,
            ConditionCode.SINGLE_PARTY_MEMBER_ALIVE,
            ConditionCode.HIT_BY_SUMMON,
            ConditionCode.NO_FEMALE_PARTY_MEMBERS_TARGETABLE
        }

    def has_unrestricted_second_byte(self) -> bool:
        '''Unrestricted as in "any value is valid".'''
        return self in {
            ConditionCode.ENEMY_SLOTS,
            ConditionCode.HIT_BY_COMMAND_WITH_ELEMENT,
            ConditionCode.HIT_BY_COMMAND_WITH_CATEGORY,
            ConditionCode.HIT_BY_SPELL,
            ConditionCode.HIT_BY_ITEM,
            ConditionCode.TARGET_COUNT
        }

    def has_irrelevant_third_byte(self) -> bool:
        '''Irrelevant as in "ignored by the game".'''
        return self in {
            ConditionCode.UNCONDITIONAL,
            ConditionCode.ENEMY_SLOTS,
            ConditionCode.TARGET_COUNT,
            ConditionCode.HP_DAMAGE_JUST_TAKEN,
            ConditionCode.DEATH_COUNTER,
            ConditionCode.SINGLE_PARTY_MEMBER_ALIVE,
            ConditionCode.HIT_BY_SUMMON,
            ConditionCode.NO_FEMALE_PARTY_MEMBERS_TARGETABLE
        }

    def has_unrestricted_third_byte(self) -> bool:
        '''Unrestricted as in "any value is valid".'''
        return self in {
            ConditionCode.HP_LOWER_THAN_THRESHOLD,
            ConditionCode.LONE_ENEMY,  # This is probably a bug in the original game, but the third byte of this condition is ignored.
            ConditionCode.HIT_BY_ITEM,
            ConditionCode.COMPARE_WITH_A2
        }

    def has_irrelevant_fourth_byte(self) -> bool:
        '''Irrelevant as in "ignored by the game".'''
        return self in {
            ConditionCode.UNCONDITIONAL,
            ConditionCode.LONE_ENEMY,
            ConditionCode.HIT_BY_SPELL,
            ConditionCode.HIT_BY_ITEM,
            ConditionCode.TARGET_COUNT,
            ConditionCode.HP_DAMAGE_JUST_TAKEN,
            ConditionCode.DEATH_COUNTER,
            ConditionCode.SINGLE_PARTY_MEMBER_ALIVE,
            ConditionCode.HIT_BY_SUMMON,
            ConditionCode.NO_FEMALE_PARTY_MEMBERS_TARGETABLE
        }

    def has_unrestricted_fourth_byte(self) -> bool:
        '''Unrestricted as in "any value is valid".'''
        return self in {
            ConditionCode.STATUS_EFFECT,  # Multiple statuses can be checked by using a bitmask in the fourth byte.
            ConditionCode.HP_LOWER_THAN_THRESHOLD,
            ConditionCode.VAR_CHECK,
            ConditionCode.ENEMY_SLOTS,  # Multiple slots can be checked by using a bitmask in the fourth byte.
            ConditionCode.HIT_BY_COMMAND_WITH_ELEMENT,  # Multiple elements can be checked by using a bitmask in the fourth byte.
            ConditionCode.HIT_BY_COMMAND_WITH_CATEGORY,  # Multiple categories can be checked by using a bitmask in the fourth byte.
            ConditionCode.PARTY_MEMBER_PARAMETER,
            ConditionCode.COMPARE_WITH_A2,
            ConditionCode.GLOBAL_EVENT_FLAGS  # Multiple flags can be checked by using a bitmask in the fourth byte.
        }
