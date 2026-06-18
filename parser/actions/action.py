from typing import Any, Optional, override
from abc import ABC, abstractmethod
from ..enums.action_code import ActionCode


class AIRuleAction(ABC):
    def __init__(self, action_code: int | ActionCode, optional_second_byte: Optional[int], optional_third_byte: Optional[int], optional_fourth_byte: Optional[int]=None) -> None:
        assert isinstance(action_code, (int, ActionCode)), "action_code must be an integer or ActionCode."
        assert optional_second_byte is None or isinstance(optional_second_byte, int), "optional_second_byte must be an integer or None."
        assert optional_third_byte is None or isinstance(optional_third_byte, int), "optional_third_byte must be an integer or None."
        assert optional_fourth_byte is None or isinstance(optional_fourth_byte, int), "optional_fourth_byte must be an integer or None."

        self.__action_code: int = action_code.value if isinstance(action_code, ActionCode) else action_code
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

    def get_tokens(self) -> list[int]:
        tokens: list[int] = [self.__action_code]

        if self.__second_byte is not None:
            tokens.append(self.__second_byte)

        if self.__third_byte is not None:
            tokens.append(self.__third_byte)

        if self.__fourth_byte is not None:
            tokens.append(self.__fourth_byte)

        return tokens

    @override
    def __str__(self) -> str:
        # No spaces.
        return "".join(filter(None, [self.hex_action_code, self.hex_second_byte, self.hex_third_byte, self.hex_fourth_byte]))

    @override
    def __repr__(self) -> str:
        # Spaces between each byte.
        return " ".join(filter(None, [self.hex_action_code, self.hex_second_byte, self.hex_third_byte, self.hex_fourth_byte]))

    @abstractmethod
    def terminates_turn_by_default(self) -> bool:
        """Indicates whether this action terminates the turn by default."""
        ...

    @abstractmethod
    def to_json(self) -> str | dict[str, Any]:
        """Converts the action to a JSON-serialisable dictionary."""
        ...

    @abstractmethod
    def to_compact_representation(self, indent: int) -> list[str]:
        """Converts the action to a compact string representation."""
        ...
