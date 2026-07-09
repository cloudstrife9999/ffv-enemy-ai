from typing import Any

from .rule import EnemyAIRule
from .enums.game_version import GameVersion
from .actions.action import AIRuleAction
from .actions.ai_command_action import AICommandAction
from .actions.no_interrupt_action import NoInterruptAction
from .actions.random_selection_action import RandomSelectionAction
from .actions.gba_random_selection_action import GBARandomSelectionAction
from .actions.simple_action import SimpleAction
from .ability import Ability
from .enums.abilities.enemy_abilities import EnemyAbilities


class EnemyAI():
    def __init__(self, enemy_id: str, enemy_name: str, enemy_special_ability: str, raw: str, game_version: GameVersion) -> None:
        self.__enemy_id: str = enemy_id
        self.__enemy_name: str = enemy_name
        self.__enemy_special_ability: str = enemy_special_ability
        self.__raw: str = raw
        self.__tokens: list[list[int]] = []
        self.__game_version: GameVersion = game_version
        self.__active_ai_rules: list[EnemyAIRule] = []
        self.__reactive_ai_rules: list[EnemyAIRule] = []
        self.__first_terminator_encountered: bool = False
        self.__parsing_condition_group: bool = True
        self.__current_rule: EnemyAIRule = EnemyAIRule(enemy_special_ability=enemy_special_ability, game_version=game_version)

    @property
    def tokens(self) -> list[list[int]]:
        return self.__tokens

    @tokens.setter
    def tokens(self, _: Any) -> None:
        raise AttributeError("Tokens property is read-only. Use add_condition(), add_action(), add_separator(), or add_terminator() to add new tokens.")

    def get_all_simple_action_names(self) -> set[str]:
        all_actions: list[AIRuleAction] = []

        for rule in self.__active_ai_rules + self.__reactive_ai_rules:
            all_actions.extend(rule.actions)

        simple_actions: set[str] = self.__extract_simple_action_names(all_actions)

        return simple_actions

    def __extract_simple_action_names(self, all_actions: list[AIRuleAction]) -> set[str]:
        simple_actions: set[str] = set()

        for action in all_actions:
            if isinstance(action, SimpleAction):
                simple_actions.add(self.__get_action_name_from_id(action.raw_action_code))
            elif isinstance(action, RandomSelectionAction) or isinstance(action, GBARandomSelectionAction):
                simple_actions.add(self.__get_action_name_from_id(action.first_choice.raw_action_code))
                simple_actions.add(self.__get_action_name_from_id(action.second_choice.raw_action_code))
                simple_actions.add(self.__get_action_name_from_id(action.third_choice.raw_action_code))
            elif isinstance(action, AICommandAction) and isinstance(action.sub_action, NoInterruptAction):
                simple_actions.update(self.__extract_simple_action_names(action.sub_action.sub_actions))

        return simple_actions

    def __get_action_name_from_id(self, action_id: int) -> str:
        if EnemyAbilities.is_valid_id(action_id) and EnemyAbilities(action_id) == EnemyAbilities.UNNAMED_SPECIAL_ABILITY:
            return self.__enemy_special_ability
        elif Ability.is_valid_id(action_id):
            return str(Ability.from_id(action_id))
        else:
            raise ValueError(f"Invalid action ID: 0x{action_id:02X}. Cannot retrieve action name.")

    def add_condition(self, tokens: list[int]) -> None:
        self.__tokens.append(tokens)

        self.__current_rule.add_condition(tokens)

    def add_action(self, tokens: list[int], battle_text: dict[int, str]) -> None:
        self.__tokens.append(tokens)

        self.__current_rule.add_action(tokens, battle_text)

    def add_separator(self, tokens: list[int]) -> None:
        self.__tokens.append(tokens)

        if not self.__parsing_condition_group and not self.__first_terminator_encountered:
            self.__active_ai_rules.append(self.__current_rule)

            self.__current_rule = EnemyAIRule(enemy_special_ability=self.__enemy_special_ability, game_version=self.__game_version)
        elif not self.__parsing_condition_group:
            self.__reactive_ai_rules.append(self.__current_rule)

            self.__current_rule = EnemyAIRule(enemy_special_ability=self.__enemy_special_ability, game_version=self.__game_version)

        self.__parsing_condition_group = not self.__parsing_condition_group  # Switching between parsing condition group and action group (or vice versa) after a separator.

    def add_terminator(self, tokens: list[int]) -> None:
        self.__tokens.append(tokens)

        if not self.__parsing_condition_group and not self.__first_terminator_encountered:
            self.__active_ai_rules.append(self.__current_rule)

            self.__current_rule = EnemyAIRule(enemy_special_ability=self.__enemy_special_ability, game_version=self.__game_version)
        elif not self.__parsing_condition_group:
            self.__reactive_ai_rules.append(self.__current_rule)

            self.__current_rule = EnemyAIRule(enemy_special_ability=self.__enemy_special_ability, game_version=self.__game_version)

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
