from typing import Any, override

from .condition import AIRuleCondition
from ..enums.condition_code import ConditionCode
from ..enums.match import MatchType
from ..enums.item import Item


class HitByExactItemCondition(AIRuleCondition):
    def __init__(self, match_type: MatchType, item: Item, fourth_byte: int) -> None:
        super().__init__(ConditionCode.HIT_BY_ITEM.value, match_type.value, item.value, fourth_byte)

    @property
    def match_type(self) -> MatchType:
        '''
        For this condition:
        - 0x00: the last item that hit the enemy matches the item ID.
        - 0x01: the last item that hit the enemy does not match the item ID.
        '''
        return MatchType(self.raw_second_byte)

    @property
    def item(self) -> Item:
        return Item(self.raw_third_byte)

    @override
    def to_json(self) -> str | dict[str, Any]:
        return {
            "condition": self.condition_code.name,
            "match_type": self.match_type.name,
            "explanation": "the item matches" if self.match_type == MatchType.MATCH else "the item does not match",
            "item": str(self.item)
        }

    @override
    def to_compact_representation(self, indent: int) -> list[str]:
        if self.match_type == MatchType.MATCH:
            return [f"{" " * indent}Hit by this item: {str(self.item)}"]
        else:
            return [f"{" " * indent}Hit by an item that is not {str(self.item)}"]
