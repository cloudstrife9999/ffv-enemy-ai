from typing import Any

from .rule import EnemyAIRule


class EnemyAI():
    def __init__(self, enemy_id: str, enemy_name: str, raw: str):
        self.__enemy_id: str = enemy_id
        self.__enemy_name: str = enemy_name
        self.__raw: str = raw
        self.__tokens: list[list[int]] = []
        self.__active_ai_rules: list[EnemyAIRule] = []
        self.__reactive_ai_rules: list[EnemyAIRule] = []
        self.__first_terminator_encountered: bool = False
        self.__parsing_condition_group: bool = True
        self.__current_rule: EnemyAIRule = EnemyAIRule()

    @property
    def tokens(self) -> list[list[int]]:
        return self.__tokens

    @tokens.setter
    def tokens(self, _: Any) -> None:
        raise AttributeError("Tokens property is read-only. Use add_condition(), add_action(), add_separator(), or add_terminator() to add new tokens.")

    def add_condition(self, tokens: list[int]) -> None:
        self.__tokens.append(tokens)

        self.__current_rule.add_condition(tokens)

    def add_action(self, tokens: list[int]) -> None:
        self.__tokens.append(tokens)

        self.__current_rule.add_action(tokens)

    def add_separator(self, tokens: list[int]) -> None:
        self.__tokens.append(tokens)

        if not self.__parsing_condition_group and not self.__first_terminator_encountered:
            self.__active_ai_rules.append(self.__current_rule)

            self.__current_rule = EnemyAIRule()
        elif not self.__parsing_condition_group:
            self.__reactive_ai_rules.append(self.__current_rule)

            self.__current_rule = EnemyAIRule()

        self.__parsing_condition_group = not self.__parsing_condition_group  # Switching between parsing condition group and action group (or vice versa) after a separator.

    def add_terminator(self, tokens: list[int]) -> None:
        self.__tokens.append(tokens)

        if not self.__parsing_condition_group and not self.__first_terminator_encountered:
            self.__active_ai_rules.append(self.__current_rule)

            self.__current_rule = EnemyAIRule()
        elif not self.__parsing_condition_group:
            self.__reactive_ai_rules.append(self.__current_rule)

            self.__current_rule = EnemyAIRule()

        if not self.__first_terminator_encountered:
            self.__first_terminator_encountered = True

        self.__parsing_condition_group = True  # After a terminator, if any tokens remain, they will be part of a new condition group.

    def finalise_no_interrupt_action(self, additional_length: bool, override_length_mismatch: bool = False) -> None:
        self.__current_rule.finalise_no_interrupt_action(additional_length, override_length_mismatch)

    def has_lingering_no_interrupt_action(self) -> bool:
        return self.__current_rule.has_lingering_no_interrupt_action()

    def compile_tokens(self) -> str:
        return "".join(f"{byte:02X}" for token in self.__tokens for byte in token)

    def to_json(self) -> dict[str, Any]:
        return {
            "enemy_id": self.__enemy_id,
            "enemy_name": self.__enemy_name,
            "raw": self.__raw,
            "active_rules": [rule.to_json(reactive=False) for rule in self.__active_ai_rules],
            "reactive_rules": [rule.to_json(reactive=True) for rule in self.__reactive_ai_rules]
        }

    def to_compact_representation(self) -> list[str]:
        return [
            "ACTIVE RULES:"
        ] + self.__format_active_rules() + [
            "REACTIVE RULES:"
        ] + self.__format_reactive_rules()

    def __format_active_rules(self) -> list[str]:
        new_lines: list[str] = []

        for i, rule in enumerate(self.__active_ai_rules):
            compact_rule_lines: list[str] = rule.to_compact_representation(reactive=False)

            if i == len(self.__active_ai_rules) - 1:
                new_lines.extend(["  Default rule:"] + [f"    {line}" for line in compact_rule_lines])
            else:
                new_lines.extend([f"  Rule #{i+1}:"] + [f"    {line}" for line in compact_rule_lines])

        return new_lines

    def __format_reactive_rules(self) -> list[str]:
        if not self.__reactive_ai_rules:
            return ["  None"]

        new_lines: list[str] = []

        for i, rule in enumerate(self.__reactive_ai_rules):
            compact_rule_lines: list[str] = rule.to_compact_representation(reactive=True)

            new_lines.extend([f"  Rule #{i+1}:"] + [f"    {line}" for line in compact_rule_lines])

        return new_lines
