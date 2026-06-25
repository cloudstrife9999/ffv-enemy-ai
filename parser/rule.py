from typing import Any, Optional, cast

from .conditions.condition import AIRuleCondition
from .actions.action import AIRuleAction
from .actions.no_interrupt_action import NoInterruptAction
from .actions.ai_command_action import AICommandAction
from .condition_factory import ConditionFactory
from .action_factory import ActionFactory
from .enums.game_version import GameVersion

class EnemyAIRule():
    def __init__(self, enemy_special_ability: str, game_version: GameVersion) -> None:
        self.__tokens: list[list[int]] = []
        self.__conditions: list[AIRuleCondition] = []
        self.__actions: list[AIRuleAction] = []
        self.__current_no_interrupt_action: Optional[AICommandAction] = None
        self.__enemy_special_ability: str = enemy_special_ability
        self.__game_version: GameVersion = game_version

    def add_condition(self, tokens: list[int]) -> None:
        self.__tokens.append(tokens)

        condition: AIRuleCondition = ConditionFactory.create_condition(self.__game_version, tokens)

        if condition:
            self.__conditions.append(condition)
        else:
            raise ValueError(f"Failed to create condition from tokens: {tokens}.")

    def add_action(self, tokens: list[int], battle_text: dict[int, str]) -> None:
        self.__tokens.append(tokens)

        action: AIRuleAction = ActionFactory.create_action(self.__game_version, tokens, battle_text, self.__enemy_special_ability)

        is_no_interrupt_action: bool = isinstance(action, AICommandAction) and isinstance(action.sub_action, NoInterruptAction)

        if not action:
            raise ValueError(f"Failed to create action from tokens: {tokens}.")
        elif is_no_interrupt_action and self.__current_no_interrupt_action is None:
            self.__current_no_interrupt_action = cast(AICommandAction, action)
        elif is_no_interrupt_action and self.__current_no_interrupt_action is not None:
            raise ValueError("Cannot add a new NoInterruptAction while another is still being constructed.")
        elif self.__current_no_interrupt_action is not None:
            self.__add_to_no_interrupt_action(action)
        else:
            self.__actions.append(action)

    def __add_to_no_interrupt_action(self, action: AIRuleAction) -> None:
        assert self.__current_no_interrupt_action is not None, "No current NoInterruptAction to add sub-action to."

        cast(NoInterruptAction, self.__current_no_interrupt_action.sub_action).add_sub_action(action)

    def finalise_no_interrupt_action(self, additional_length: bool, override_length_mismatch: bool = False) -> None:
        if self.__current_no_interrupt_action is None:
            raise ValueError("No current NoInterruptAction to mark.")
        elif additional_length:
            cast(NoInterruptAction, self.__current_no_interrupt_action.sub_action).mark_separator_or_terminator_included_in_length()

        cast(NoInterruptAction, self.__current_no_interrupt_action.sub_action).validate_complete_action(override_length_mismatch=override_length_mismatch)

        self.__actions.append(self.__current_no_interrupt_action)

        self.__current_no_interrupt_action = None

    def has_lingering_no_interrupt_action(self) -> bool:
        return self.__current_no_interrupt_action is not None

    def to_json(self, reactive: bool) -> dict[str, Any]:
        return {
            "conditions": [condition.to_json() for condition in self.__conditions],
            "actions": {f"Turn #{i+1}": action.to_json() for i, action in enumerate(self.__actions)} if not reactive else [action.to_json() for action in self.__actions]
        }

    def to_compact_representation(self, reactive: bool) -> list[str]:
        if reactive:
            return [
                "Conditions:"
            ] + [
                condition_line for condition in self.__conditions for condition_line in condition.to_compact_representation(indent=2)
            ] + [
                "Actions:"
            ] + [
                action_line for action in self.__actions for action_line in action.to_compact_representation(indent=2)
            ]        
        else:
            return [
                "Conditions:"
            ] + [
                condition_line for condition in self.__conditions for condition_line in condition.to_compact_representation(indent=2)
            ] + [
                "Actions:"
            ] + self.__add_turn_numbers_to_actions()

    def __add_turn_numbers_to_actions(self) -> list[str]:
        new_lines: list[str] = []
        new_turn: bool = True
        turn_number: int = 1

        for action in self.__actions:
            action_lines: list[str] = action.to_compact_representation(indent=2)
            prefix: str = f"Turn #{turn_number}: "

            for j, line in enumerate(action_lines):
                existing_leading_spaces: int = len(line) - len(line.lstrip())

                if j == 0 and new_turn:
                    line = " " * existing_leading_spaces + prefix + line.lstrip()

                    new_turn = False
                else:
                    line = " " * (existing_leading_spaces + len(prefix)) + line.lstrip()

                action_lines[j] = line

            new_lines.extend(action_lines)

            if action.terminates_turn_by_default():
                new_turn = True
                turn_number += 1

        return new_lines
