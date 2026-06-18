from typing import Any, override

from .condition import AIRuleCondition
from ..enums.condition_code import ConditionCode
from ..enums.match import MatchType
from ..enums.command import Command
from ..enums.element import Element


class HitByCommandCondition(AIRuleCondition):
    def __init__(self, condition_code: ConditionCode, match_type: MatchType, command: Command, elemental_mask: int) -> None:
        super().__init__(condition_code.value, match_type.value, command.value, elemental_mask)

        if condition_code not in [ConditionCode.HIT_BY_COMMAND, ConditionCode.HIT_BY_COMMAND_CLASS]:
            raise ValueError(f"Invalid condition code for HitByCommandCondition: {condition_code}.")

    @property
    def match_type(self) -> MatchType:
        '''
        For this condition:
        - 0x00: the last command that hit the enemy matches both the command ID and elemental mask.
        - 0x01: the last command that hit the enemy either does not match the command ID or does not match the elemental mask (or does not match either).
        '''
        return MatchType(self.raw_second_byte)

    @property
    def command(self) -> Command:
        return Command(self.raw_third_byte)

    @property
    def elemental_mask(self) -> int:
        return self.raw_fourth_byte

    @property
    def elements(self) -> list[Element]:
        return Element.from_mask(self.elemental_mask)

    @override
    def to_json(self) -> str | dict[str, Any]:
        return {
            "condition": self.condition_code.name,
            "match_type": self.match_type.name,
            "explanation": "both command and elements match" if self.match_type == MatchType.MATCH else "either the command or the elements or both do not match",
            "command": str(self.command),
            "elements": [element.name.capitalize() for element in self.elements] if self.elements else "irrelevant (including non-elemental)"
        }

    @override
    def to_compact_representation(self, indent: int) -> list[str]:
        if self.match_type == MatchType.MATCH and self.elements:
            return [f"{" " * indent}Hit by {str(self.command)} using any of the following elements: {[str(element) for element in self.elements]}"]
        elif self.elements:
            return [f"{" " * indent}Hit by a command other than {str(self.command)} or hit by it with an elemental action that does not match any of {[str(element) for element in self.elements]}"]
        elif self.match_type == MatchType.MATCH:
            return [f"{" " * indent}Hit by {str(self.command)}"]
        else:
            return [f"{" " * indent}Hit by a command other than {str(self.command)}"]
