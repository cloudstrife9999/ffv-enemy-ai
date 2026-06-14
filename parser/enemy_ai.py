from typing import Any

from .rule import EnemyAIRule


# TODO: Implement this.
class EnemyAI():
    def __init__(self, enemy_id: str, enemy_name: str, raw: str, tokens: list[list[int]]):
        self.__enemy_id: str = enemy_id
        self.__enemy_name: str = enemy_name
        self.__raw: str = raw
        self.__tokens: list[list[int]] = tokens
        self.__active_ai_rules: list[EnemyAIRule] = []
        self.__reactive_ai_rules: list[EnemyAIRule] = []

    def to_json(self) -> dict[str, Any]:
        return {
            "enemy_id": self.__enemy_id,
            "enemy_name": self.__enemy_name,
            "raw": self.__raw,
            "active_rules": [rule.to_json() for rule in self.__active_ai_rules],
            "reactive_rules": [rule.to_json() for rule in self.__reactive_ai_rules]
        }
