from typing import Any, override

from .condition import AIRuleCondition
from ..enums.condition_code import ConditionCode
from ..enums.match import MatchType
from ..enums.abilities.enemy_abilities import EnemyAbilities
from ..ability import Ability, GenericAbility


class HitByExactSpellCondition(AIRuleCondition):
    def __init__(self, match_type: MatchType, spell: GenericAbility, fourth_byte: int) -> None:
        super().__init__(ConditionCode.HIT_BY_SPELL.value, match_type.value, spell.value, fourth_byte)

    @property
    def match_type(self) -> MatchType:
        '''
        For this condition:
        - 0x00: the last spell that hit the enemy matches the spell ID.
        - 0x01: the last spell that hit the enemy does not match the spell ID.
        '''
        return MatchType(self.raw_second_byte)

    @property
    def spell(self) -> GenericAbility:
        return Ability.from_id(self.raw_third_byte)

    @override
    def to_json(self) -> str | dict[str, Any]:
        return {
            "condition": str(self.condition_code),
            "match_type": str(self.match_type),
            "explanation": "the ability matches" if self.match_type == MatchType.MATCH else "the ability does not match",
            "ability": str(self.spell)
        }

    @override
    def to_compact_representation(self, indent: int) -> list[str]:
        spell_name: str = str(self.spell)

        if self.match_type == MatchType.MATCH and self.spell is EnemyAbilities.UNNAMED_SCRIPT_TRIGGER:
            return [f"{" " * indent}Hit by the unnamed script trigger spell"]
        elif self.match_type == MatchType.MATCH:
            return [f"{" " * indent}Hit by the {spell_name} spell"]
        elif self.match_type == MatchType.NO_MATCH and self.spell is EnemyAbilities.UNNAMED_SCRIPT_TRIGGER:
            return [f"{" " * indent}Hit by a spell other than the unnamed script trigger"]
        elif self.match_type == MatchType.NO_MATCH:
            return [f"{" " * indent}Hit by a spell other than {spell_name}"]
        else:
            raise ValueError(f"Invalid match type: {self.match_type}.")
