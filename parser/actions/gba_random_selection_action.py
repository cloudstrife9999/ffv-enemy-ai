from typing import Any, override


from .action import AIRuleAction
from .simple_action import SimpleAction
from ..enums.action_code import ActionCode


class GBARandomSelectionAction(AIRuleAction):
    def __init__(self, first_choice: SimpleAction, second_choice: SimpleAction, third_choice: SimpleAction) -> None:
        super().__init__(action_code=ActionCode.GBA_RANDOM_SELECTION, optional_second_byte=first_choice.raw_action_code, optional_third_byte=second_choice.raw_action_code, optional_fourth_byte=third_choice.raw_action_code)

    @property
    def first_choice(self) -> SimpleAction:
        if self.raw_second_byte is None:
            raise ValueError("First choice action code is not set.")
        else:
            return SimpleAction(self.raw_second_byte)

    @property
    def second_choice(self) -> SimpleAction:
        if self.raw_third_byte is None:
            raise ValueError("Second choice action code is not set.")
        else:
            return SimpleAction(self.raw_third_byte)

    @property
    def third_choice(self) -> SimpleAction:
        if self.raw_fourth_byte is None:
            raise ValueError("Third choice action code is not set.")
        else:
            return SimpleAction(self.raw_fourth_byte)

    @override
    def to_json(self) -> str | dict[str, Any]:
        return {
            "action": self.action_code.name,
            "first_choice": self.first_choice.to_json(),
            "second_choice": self.second_choice.to_json(),
            "third_choice": self.third_choice.to_json()
        }
