from enum import Enum
from typing import override


class Variable(Enum):
    VAR_00 = 0x00
    VAR_01 = 0x01
    VAR_02 = 0x02
    VAR_03 = 0x03

    @override
    def __str__(self) -> str:
        return self.name.title()

    @classmethod
    def is_valid_var_id(cls, value: int) -> bool:
        return value in cls._value2member_map_
