from typing import Any, Optional, override
from abc import ABC, abstractmethod
from ..enums.action_code import ActionCode


class AIRuleAction(ABC):
    def __init__(self, action_code: int, optional_second_byte: Optional[int], optional_third_byte: Optional[int], optional_fourth_byte: Optional[int]=None) -> None:
        self.__action_code: int = action_code
        self.__second_byte: Optional[int] = optional_second_byte
        self.__third_byte: Optional[int] = optional_third_byte
        self.__fourth_byte: Optional[int] = optional_fourth_byte

    @property
    def action_code(self) -> ActionCode:
        return ActionCode(self.__action_code)

    @property
    def raw_action_code(self) -> int:
        return self.__action_code

    @property
    def hex_action_code(self) -> str:
        return f"{self.__action_code:02X}"

    @property
    def qualified_hex_action_code(self) -> str:
        return f"0x{self.__action_code:02X}"

    @raw_action_code.setter
    def raw_action_code(self, _: Any) -> None:
        raise AttributeError("raw_action_code is read-only.")

    @property
    def raw_second_byte(self) -> Optional[int]:
        return self.__second_byte

    @property
    def hex_second_byte(self) -> Optional[str]:
        return f"{self.__second_byte:02X}" if self.__second_byte is not None else None

    @property
    def qualified_hex_second_byte(self) -> Optional[str]:
        return f"0x{self.__second_byte:02X}" if self.__second_byte is not None else None

    @raw_second_byte.setter
    def raw_second_byte(self, _: Any) -> None:
        raise AttributeError("raw_second_byte is read-only.")

    @property
    def raw_third_byte(self) -> Optional[int]:
        return self.__third_byte

    @property
    def hex_third_byte(self) -> Optional[str]:
        return f"{self.__third_byte:02X}" if self.__third_byte is not None else None

    @property
    def qualified_hex_third_byte(self) -> Optional[str]:
        return f"0x{self.__third_byte:02X}" if self.__third_byte is not None else None

    @raw_third_byte.setter
    def raw_third_byte(self, _: Any) -> None:
        raise AttributeError("raw_third_byte is read-only.")

    @property
    def raw_fourth_byte(self) -> Optional[int]:
        return self.__fourth_byte

    @property
    def hex_fourth_byte(self) -> Optional[str]:
        return f"{self.__fourth_byte:02X}" if self.__fourth_byte is not None else None

    @property
    def qualified_hex_fourth_byte(self) -> Optional[str]:
        return f"0x{self.__fourth_byte:02X}" if self.__fourth_byte is not None else None

    @raw_fourth_byte.setter
    def raw_fourth_byte(self, _: Any) -> None:
        raise AttributeError("raw_fourth_byte is read-only.")

    @property
    def length(self) -> int:
        length: int = 1  # Start with the action code byte

        if self.__second_byte is not None:
            length += 1

        if self.__third_byte is not None:
            length += 1

        if self.__fourth_byte is not None:
            length += 1

        return length

    @override
    def __str__(self) -> str:
        # No spaces.
        return f"{self.hex_action_code}{self.hex_second_byte}{self.hex_third_byte}{self.hex_fourth_byte}"

    @override
    def __repr__(self) -> str:
        # Spaces between each byte.
        return f"{self.hex_action_code} {self.hex_second_byte} {self.hex_third_byte} {self.hex_fourth_byte}"

    @abstractmethod
    def to_json(self) -> str | dict[str, Any]:
        """Converts the action to a JSON-serialisable dictionary."""
        ...
