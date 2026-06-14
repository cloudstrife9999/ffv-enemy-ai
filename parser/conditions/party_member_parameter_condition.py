from typing import Any, override

from .condition import AIRuleCondition
from ..enums.condition_code import ConditionCode
from ..enums.target import Target
from ..enums.party_member import PartyMemberParameter


class PartyMemberParameterCondition(AIRuleCondition):
    def __init__(self, target: Target, parameter: PartyMemberParameter, expected_value: int) -> None:
        super().__init__(ConditionCode.PARTY_MEMBER_PARAMETER.value, target.value, parameter.value, expected_value)

    @property
    def target(self) -> Target:
        return Target(self.raw_second_byte)

    @property
    def parameter(self) -> PartyMemberParameter:
        return PartyMemberParameter(self.raw_third_byte)

    @property
    def expected_value(self) -> int:
        return self.raw_fourth_byte

    @override
    def to_json(self) -> str | dict[str, Any]:
        return {
            "condition_code": self.condition_code.name,
            "target": self.target.name,
            "parameter": self.parameter.name,
            "expected_value": self.expected_value
        }
