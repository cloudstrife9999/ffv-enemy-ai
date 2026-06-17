from typing import Any, Optional, cast

from .conditions.condition import AIRuleCondition
from .actions.action import AIRuleAction
from .actions.no_interrupt_action import NoInterruptAction
from .actions.ai_command_action import AICommandAction
from .condition_factory import ConditionFactory
from .action_factory import ActionFactory

class EnemyAIRule():
    def __init__(self):
        self.__tokens: list[list[int]] = []
        self.__conditions: list[AIRuleCondition] = []
        self.__actions: list[AIRuleAction] = []
        self.__current_no_interrupt_action: Optional[AICommandAction] = None

    def add_condition(self, tokens: list[int]) -> None:
        self.__tokens.append(tokens)

        condition: AIRuleCondition = ConditionFactory.create_condition(tokens)

        if condition:
            self.__conditions.append(condition)
        else:
            raise ValueError(f"Failed to create condition from tokens: {tokens}.")

    def add_action(self, tokens: list[int]) -> None:
        self.__tokens.append(tokens)

        action: AIRuleAction = ActionFactory.create_action(tokens)

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

    def to_json(self) -> dict[str, list[str | dict[str, Any]]]:
        return {
            "conditions": [condition.to_json() for condition in self.__conditions],
            "actions": [action.to_json() for action in self.__actions]
        }
