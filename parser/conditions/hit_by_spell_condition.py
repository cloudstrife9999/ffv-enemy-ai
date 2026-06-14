from typing import Any, override

from .condition import AIRuleCondition
from ..enums.condition_code import ConditionCode
from ..enums.match import MatchType
from ..enums.ability import Ability


class HitByExactSpellCondition(AIRuleCondition):
    def __init__(self, match_type: MatchType, spell: Ability, fourth_byte: int) -> None:
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
    def spell(self) -> Ability:
        return Ability(self.raw_third_byte)

    @override
    def to_json(self) -> str | dict[str, Any]:
        return {
            "condition": self.condition_code.name,
            "match_type": self.match_type.name,
            "explanation": "the ability matches" if self.match_type == MatchType.MATCH else "the ability does not match",
            "ability": self.spell.name
        }
