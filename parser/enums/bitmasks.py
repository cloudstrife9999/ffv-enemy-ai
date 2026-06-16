from enum import IntEnum


class Bitmask(IntEnum):
    BIT_7 = 0x80
    BIT_6 = 0x40
    BIT_5 = 0x20
    BIT_4 = 0x10
    BIT_3 = 0x08
    BIT_2 = 0x04
    BIT_1 = 0x02
    BIT_0 = 0x01

    @classmethod
    def is_valid_bitmask(cls, value: int) -> bool:
        return value in cls._value2member_map_
