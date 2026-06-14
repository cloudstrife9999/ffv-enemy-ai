from .conditions.condition import AIRuleCondition
from .conditions.unconditional import Unconditional
from .conditions.status_effect_condition import StatusEffectCondition
from .conditions.hp_threshold_condition import HPThresholdCondition
from .conditions.var_check_condition import VarCheckCondition
from .conditions.lone_enemy_condition import LoneEnemyCondition
from .conditions.enemy_slots_condition import EnemySlotsCondition
from .conditions.hit_by_command_condition import HitByCommandCondition
from .conditions.hit_by_spell_condition import HitByExactSpellCondition
from .conditions.hit_by_item_condition import HitByExactItemCondition
from .conditions.target_count_condition import TargetCountCondition
from .conditions.party_member_parameter_condition import PartyMemberParameterCondition
from .conditions.a2_comparison import A2ComparisonCondition
from .conditions.global_event_condition import GlobalEventCondition
from .conditions.hp_damage_condition import HPDamageCondition
from .conditions.death_counter_condition import DeathCounterCondition
from .conditions.single_party_member_alive_condition import SinglePartyMemberAliveCondition
from .conditions.hit_by_summon_condition import HitBySummonCondition
from .conditions.no_female_targets import NoFemalePartyMembersTargetableCondition
from .enums.condition_code import ConditionCode
from .enums.target import Target
from .enums.status_table import StatusTable
from .enums.match import MatchType
from .enums.variable import Variable
from .enums.command import Command
from .enums.ability import Ability
from .enums.item import Item
from .enums.target_count import TargetCount
from .enums.party_member_offset import PartyMemberPropertyTable
from .enums.global_event_table import GlobalEventTable


class ConditionFactory():
    @staticmethod
    def create_condition(bytes: list[int]) -> AIRuleCondition:
        if len(bytes) != 4:
            raise ValueError("A valid condition must be 4 bytes long.")
        else:
            condition_code: int = bytes[0] & 0xFF
            second_byte: int = bytes[1] & 0xFF
            third_byte: int = bytes[2] & 0xFF
            fourth_byte: int = bytes[3] & 0xFF

            return ConditionFactory.__create_condition_from_bytes(condition_code, second_byte, third_byte, fourth_byte)

    @staticmethod
    def __create_condition_from_bytes(condition_code: int, second_byte: int, third_byte: int, fourth_byte: int) -> AIRuleCondition:
        try:
            match ConditionCode(condition_code):
                case ConditionCode.UNCONDITIONAL:
                    return Unconditional(second_byte=second_byte, third_byte=third_byte, fourth_byte=fourth_byte)
                case ConditionCode.STATUS_EFFECT:
                    return StatusEffectCondition(target=Target(second_byte), status_table_number=StatusTable(third_byte), mask=fourth_byte)
                case ConditionCode.HP_LOWER_THAN_THRESHOLD:
                    return HPThresholdCondition(target=Target(second_byte), hp_threshold_lsb=third_byte, hp_threshold_msb=fourth_byte)
                case ConditionCode.VAR_CHECK:
                    return VarCheckCondition(match_type=MatchType(second_byte), var_id=Variable(third_byte), value_to_match=fourth_byte)
                case ConditionCode.LONE_ENEMY:
                    return LoneEnemyCondition(second_byte=second_byte, third_byte=third_byte, fourth_byte=fourth_byte)
                case ConditionCode.ENEMY_SLOTS:
                    return EnemySlotsCondition(match_type=MatchType(second_byte), third_byte=third_byte, mask=fourth_byte)
                case ConditionCode.HIT_BY_COMMAND | ConditionCode.HIT_BY_COMMAND_CLASS:
                    return HitByCommandCondition(condition_code=ConditionCode(condition_code), match_type=MatchType(second_byte), command=Command(third_byte), elemental_mask=fourth_byte)
                case ConditionCode.HIT_BY_SPELL:
                    return HitByExactSpellCondition(match_type=MatchType(second_byte), spell=Ability(third_byte), fourth_byte=fourth_byte)
                case ConditionCode.HIT_BY_ITEM:
                    return HitByExactItemCondition(match_type=MatchType(second_byte), item=Item(third_byte), fourth_byte=fourth_byte)
                case ConditionCode.TARGET_COUNT:
                    return TargetCountCondition(target_count=TargetCount(second_byte), third_byte=third_byte, fourth_byte=fourth_byte)
                case ConditionCode.PARTY_MEMBER_PARAMETER:
                    return PartyMemberParameterCondition(target=Target(second_byte), property_table=PartyMemberPropertyTable(third_byte), expected_value=fourth_byte)
                case ConditionCode.COMPARE_WITH_A2:
                    return A2ComparisonCondition(second_byte=second_byte, value_lsb=third_byte, value_msb=fourth_byte)
                case ConditionCode.GLOBAL_EVENT_FLAGS:
                    return GlobalEventCondition(second_byte=second_byte, global_event_table_number=GlobalEventTable(third_byte), mask=fourth_byte)
                case ConditionCode.HP_DAMAGE_JUST_TAKEN:
                    return HPDamageCondition(second_byte=second_byte, third_byte=third_byte, fourth_byte=fourth_byte)
                case ConditionCode.DEATH_COUNTER:
                    return DeathCounterCondition(second_byte=second_byte, third_byte=third_byte, fourth_byte=fourth_byte)
                case ConditionCode.SINGLE_PARTY_MEMBER_ALIVE:
                    return SinglePartyMemberAliveCondition(second_byte=second_byte, third_byte=third_byte, fourth_byte=fourth_byte)
                case ConditionCode.HIT_BY_SUMMON:
                    return HitBySummonCondition(second_byte=second_byte, third_byte=third_byte, fourth_byte=fourth_byte)
                case ConditionCode.NO_FEMALE_PARTY_MEMBERS_TARGETABLE:
                    return NoFemalePartyMembersTargetableCondition(second_byte=second_byte, third_byte=third_byte, fourth_byte=fourth_byte)
                case _:
                    raise ValueError(f"{condition_code} is not a valid {ConditionCode.__name__}.")
        except ValueError as e:
            raise ValueError(f"Invalid condition code: {condition_code}. Error: {e}") from e
        except Exception as e:
            raise ValueError(f"Error creating condition with code {condition_code}: {e}") from e
