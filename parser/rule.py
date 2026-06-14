from typing import Any

from .conditions.condition import AIRuleCondition
from .actions.action import AIRuleAction


# TODO: Implement this.
class EnemyAIRule():
    def __init__(self, tokens: list[list[int]]):
        self.__tokens: list[list[int]] = tokens
        self.__conditions: list[AIRuleCondition] = []
        self.__actions: list[AIRuleAction] = []

    def to_json(self) -> dict[str, list[str | dict[str, Any]]]:
        return {
            "conditions": [condition.to_json() for condition in self.__conditions],
            "actions": [action.to_json() for action in self.__actions]
        }
