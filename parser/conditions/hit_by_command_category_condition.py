from typing import Any, override

from .condition import AIRuleCondition
from ..enums.condition_code import ConditionCode
from ..enums.match import MatchType
from ..enums.command import Command
from ..enums.action_category import ActionCategory


class HitByCommandWithActionCategoryCondition(AIRuleCondition):
    def __init__(self, match_type: MatchType, command: Command, category_mask: int) -> None:
        super().__init__(ConditionCode.HIT_BY_COMMAND_WITH_CATEGORY.value, match_type.value, command.value, category_mask)

    @property
    def match_type(self) -> MatchType:
        '''
        For this condition:
        - 0x00: the last command that hit the enemy matches both the command ID and action category mask.
        - 0x01: the last command that hit the enemy either does not match the command ID or does not match the action category mask (or does not match either).
        '''
        return MatchType(self.raw_second_byte)

    @property
    def command(self) -> Command:
        return Command(self.raw_third_byte)

    @property
    def category_mask(self) -> int:
        return self.raw_fourth_byte

    @property
    def categories(self) -> list[ActionCategory]:
        return ActionCategory.from_mask(self.category_mask)

    @override
    def to_json(self) -> str | dict[str, Any]:
        return {
            "condition": str(self.condition_code),
            "match_type": str(self.match_type),
            "explanation": "both command and categories match" if self.match_type == MatchType.MATCH else "either the command or the categories or both do not match",
            "command": str(self.command),
            "categories": [category.name.capitalize() for category in self.categories] if self.categories else "irrelevant"
        }

    @override
    def to_compact_representation(self, indent: int) -> list[str]:
        if self.match_type == MatchType.MATCH and self.categories:
            return [f"{" " * indent}Hit by {str(self.command)} using any of the following categories: {[str(category) for category in self.categories]}"]
        elif self.categories:
            return [f"{" " * indent}Hit by a command other than {str(self.command)} or hit by it with an action whose category does not match any of {[str(category) for category in self.categories]}"]
        elif self.match_type == MatchType.MATCH:
            return [f"{" " * indent}Hit by {str(self.command)}"]
        else:
            return [f"{" " * indent}Hit by a command other than {str(self.command)}"]
