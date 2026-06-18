from typing import Any, override

from .action import AIRuleAction
from ..enums.action_code import ActionCode
from ..enums.variable import Variable


class SetVariableAction(AIRuleAction):
    def __init__(self, var_id: Variable, value: int) -> None:
        super().__init__(action_code=ActionCode.SET_VARIABLE, optional_second_byte=var_id.value, optional_third_byte=value, optional_fourth_byte=None)

    @property
    def var_id(self) -> Variable:
        if self.raw_second_byte is None:
            raise ValueError("Variable ID is not set.")
        else:
            return Variable(self.raw_second_byte)

    @property
    def value(self) -> int:
        if self.raw_third_byte is None:
            raise ValueError("Value is not set.")
        else:
            return self.raw_third_byte

    @override
    def to_json(self) -> str | dict[str, Any]:
        return {
            "action": self.action_code.name,
            "var_id": str(self.var_id),
            "value": self.value
        }

    @override
    def to_compact_representation(self, indent: int) -> list[str]:
        return [f"{" " * indent}Set {str(self.var_id)} to {self.value}"]
