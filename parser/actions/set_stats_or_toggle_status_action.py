
from typing import Any, override

from .action import AIRuleAction
from ..enums.action_code import ActionCode
from ..enums.party_member import PartyMemberParameter


class SetStatsOrToggleStatusAction(AIRuleAction):
    def __init__(self, parameter: PartyMemberParameter, value_msb: int) -> None:
        super().__init__(action_code=ActionCode.SET_STATS_OR_TOGGLE_STATUS, optional_second_byte=parameter.value, optional_third_byte=value_msb, optional_fourth_byte=None)

    @property
    def parameter(self) -> PartyMemberParameter:
        if not self.raw_second_byte:
            raise ValueError("Party member parameter is not set.")
        else:
            return PartyMemberParameter(self.raw_second_byte)

    @property
    def value_msb(self) -> int:
        if not self.raw_third_byte:
            raise ValueError("Value MSB is not set.")
        else:
            return self.raw_third_byte

    @override
    def to_json(self) -> str | dict[str, Any]:
        return {
            "action": self.action_code.name,
            "parameter": self.parameter.name,
            "value_msb": self.value_msb
        }
