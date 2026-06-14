from enum import IntEnum
from typing import override


class ConditionCode(IntEnum):
    UNCONDITIONAL = 0x00
    STATUS_EFFECT = 0x01
    HP_LOWER_THAN_THRESHOLD = 0x02
    VAR_CHECK = 0x03
    LONE_ENEMY = 0x04
    ENEMY_SLOTS = 0x05
    HIT_BY_COMMAND = 0x06
    HIT_BY_COMMAND_CLASS = 0x07
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
            case ConditionCode.HIT_BY_COMMAND | ConditionCode.HIT_BY_COMMAND_CLASS:
                return "Hit by command"
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
