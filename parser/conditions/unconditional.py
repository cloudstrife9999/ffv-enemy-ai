from typing import Any, override

from .condition import AIRuleCondition
from ..enums.condition_code import ConditionCode


class Unconditional(AIRuleCondition):
    def __init__(self, second_byte: int=0x00, third_byte: int=0x00, fourth_byte: int=0x00) -> None:
        super().__init__(ConditionCode.UNCONDITIONAL.value, second_byte, third_byte, fourth_byte)

    @override
    def to_json(self) -> str | dict[str, Any]:
        return self.condition_code.name
