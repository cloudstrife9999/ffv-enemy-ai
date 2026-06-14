from typing import Any, override
from abc import ABC, abstractmethod

from ..enums.condition_code import ConditionCode


class AIRuleCondition(ABC):
    def __init__(self, condition_code: int, second_byte: int, third_byte: int, fourth_byte: int) -> None:
        self.__condition_code: int = condition_code
        self.__second_byte: int = second_byte
        self.__third_byte: int = third_byte
        self.__fourth_byte: int = fourth_byte

    @property
    def condition_code(self) -> ConditionCode:
        return ConditionCode(self.__condition_code)

    @property
    def raw_condition_code(self) -> int:
        return self.__condition_code

    @property
    def hex_condition_code(self) -> str:
        return f"{self.__condition_code:02X}"

    @property
    def qualified_hex_condition_code(self) -> str:
        return f"0x{self.__condition_code:02X}"

    @raw_condition_code.setter
    def raw_condition_code(self, _: Any) -> None:
        raise AttributeError("raw_condition_code is read-only.")

    @property
    def raw_second_byte(self) -> int:
        return self.__second_byte

    @property
    def hex_second_byte(self) -> str:
        return f"{self.__second_byte:02X}"

    @property
    def qualified_hex_second_byte(self) -> str:
        return f"0x{self.__second_byte:02X}"    

    @raw_second_byte.setter
    def raw_second_byte(self, _: Any) -> None:
        raise AttributeError("raw_second_byte is read-only.")

    @property
    def raw_third_byte(self) -> int:
        return self.__third_byte

    @property
    def hex_third_byte(self) -> str:
        return f"{self.__third_byte:02X}"

    @property
    def qualified_hex_third_byte(self) -> str:
        return f"0x{self.__third_byte:02X}"

    @raw_third_byte.setter
    def raw_third_byte(self, _: Any) -> None:
        raise AttributeError("raw_third_byte is read-only.")

    @property
    def raw_fourth_byte(self) -> int:
        return self.__fourth_byte

    @property
    def hex_fourth_byte(self) -> str:
        return f"{self.__fourth_byte:02X}"

    @property
    def qualified_hex_fourth_byte(self) -> str:
        return f"0x{self.__fourth_byte:02X}"

    @raw_fourth_byte.setter
    def raw_fourth_byte(self, _: Any) -> None:
        raise AttributeError("raw_fourth_byte is read-only.")

    @override
    def __str__(self) -> str:
        # No spaces.
        return f"{self.hex_condition_code}{self.hex_second_byte}{self.hex_third_byte}{self.hex_fourth_byte}"

    @override
    def __repr__(self) -> str:
        # Spaces between each byte.
        return f"{self.hex_condition_code} {self.hex_second_byte} {self.hex_third_byte} {self.hex_fourth_byte}"

    @abstractmethod
    def to_json(self) -> str | dict[str, Any]:
        """Converts the condition to a JSON-serialisable dictionary."""
        ...
