from typing import Any, override

from .action import AIRuleAction
from ..enums.action_code import ActionCode


# TODO: Find out the mapping between the second and third bytes and the actual full screen effect that is applied. For now, just store the raw values.
class FullScreenEffectAction(AIRuleAction):
    def __init__(self, second_byte: int, third_byte: int) -> None:
        super().__init__(action_code=ActionCode.FULL_SCREEN_EFFECT, optional_second_byte=second_byte, optional_third_byte=third_byte, optional_fourth_byte=None)

    @property
    def second_byte(self) -> int:
        if self.raw_second_byte is None:
            raise ValueError("Second byte is not set.")
        else:
            return self.raw_second_byte

    @property
    def third_byte(self) -> int:
        if self.raw_third_byte is None:
            raise ValueError("Third byte is not set.")
        else:
            return self.raw_third_byte

    @override
    def terminates_turn_by_default(self) -> bool:
        return False

    @override
    def to_json(self) -> str | dict[str, Any]:
        return {
            "action": self.action_code.name,
            "second_byte": self.second_byte,
            "third_byte": self.third_byte
        }

    @override
    def to_compact_representation(self, indent: int) -> list[str]:
        return [f"{" " * indent}Full screen effect: second byte = {self.second_byte}, third byte = {self.third_byte}"]