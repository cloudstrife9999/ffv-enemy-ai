from typing import Any, override

from .condition import AIRuleCondition
from ..enums.condition_code import ConditionCode
from ..enums.match import MatchType
from ..enums.variable import Variable


class VarCheckCondition(AIRuleCondition):
    def __init__(self, match_type: MatchType, var_id: Variable, value_to_match: int) -> None:
        super().__init__(ConditionCode.VAR_CHECK.value, match_type.value, var_id.value, value_to_match)

    @property
    def match_type(self) -> MatchType:
        return MatchType(self.raw_second_byte)

    @property
    def var_id(self) -> Variable:
        return Variable(self.raw_third_byte)

    @property
    def value_to_match(self) -> int:
        return self.raw_fourth_byte

    @override
    def to_json(self) -> str | dict[str, Any]:
        return {
            "condition": self.condition_code.name,
            "match_type": self.match_type.name,
            "explanation": "variable == value" if self.match_type == MatchType.MATCH else "variable != value",
            "var_id": self.var_id.name,
            "value_to_match": self.value_to_match
        }
