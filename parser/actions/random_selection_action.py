
from typing import Any, override

from .action import AIRuleAction
from .simple_action import SimpleAction
from ..enums.action_code import ActionCode


class RandomSelectionAction(AIRuleAction):
    def __init__(self, first_choice: SimpleAction, second_choice: SimpleAction, third_choice: SimpleAction, enemy_special_ability: str) -> None:
        super().__init__(action_code=ActionCode.RANDOM_SELECTION, optional_second_byte=first_choice.raw_action_code, optional_third_byte=second_choice.raw_action_code, optional_fourth_byte=third_choice.raw_action_code)

        self.__enemy_special_ability: str = enemy_special_ability

    @property
    def first_choice(self) -> SimpleAction:
        if self.raw_second_byte is None:
            raise ValueError("First choice action code is not set.")
        else:
            return SimpleAction(self.raw_second_byte, enemy_special_ability=self.__enemy_special_ability)

    @property
    def second_choice(self) -> SimpleAction:
        if self.raw_third_byte is None:
            raise ValueError("Second choice action code is not set.")
        else:
            return SimpleAction(self.raw_third_byte, enemy_special_ability=self.__enemy_special_ability)

    @property
    def third_choice(self) -> SimpleAction:
        if self.raw_fourth_byte is None:
            raise ValueError("Third choice action code is not set.")
        else:
            return SimpleAction(self.raw_fourth_byte, enemy_special_ability=self.__enemy_special_ability)

    @override
    def terminates_turn_by_default(self) -> bool:
        return True

    @override
    def to_json(self) -> str | dict[str, Any]:
        return {
            "action": "Random selection",
            "first_choice": self.first_choice.to_json(),
            "second_choice": self.second_choice.to_json(),
            "third_choice": self.third_choice.to_json()
        }

    @override
    def to_compact_representation(self, indent: int) -> list[str]:
        first_choice_repr: str = RandomSelectionAction.__format_choice_repr(self.first_choice.to_compact_representation(0)[0])
        second_choice_repr: str = RandomSelectionAction.__format_choice_repr(self.second_choice.to_compact_representation(0)[0])
        third_choice_repr: str = RandomSelectionAction.__format_choice_repr(self.third_choice.to_compact_representation(0)[0])

        return [f"{" " * indent}random({first_choice_repr}, {second_choice_repr}, {third_choice_repr})"]


    @staticmethod
    def __format_choice_repr(choice_repr: str) -> str:
        if choice_repr.strip().startswith("Ability: "):
            return choice_repr.replace("Ability: ", "")
        else:
            return choice_repr