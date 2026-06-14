
from typing import Optional, Any, override

from .action import AIRuleAction
from ..enums.action_code import ActionCode
from ..enums.target import Target


class SetTargetAction(AIRuleAction):
    def __init__(self, target: Target, optional_third_byte: Optional[int]=None) -> None:
        super().__init__(action_code=ActionCode.SET_TARGET, optional_second_byte=target.value, optional_third_byte=optional_third_byte, optional_fourth_byte=None)

    @property
    def target(self) -> Target:
        if not self.raw_second_byte:
            raise ValueError("Target is not set.")
        else:
            return Target(self.raw_second_byte)

    @override
    def to_json(self) -> str | dict[str, Any]:
        return {
            "action": self.action_code.name,
            "target": self.target.name
        }
