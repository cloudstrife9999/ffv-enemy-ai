from __future__ import annotations
from enum import IntEnum
from typing import override


class TransformationFlags(IntEnum):
    # Flags
    DO_NOT_TRANSFER_HP = 0x80  # Bit 7 set.
    TRANSFER_HP = 0x7F  # Bit 7 not set. Not a proper flag, but used to indicate that HP should be transferred to the newly shown enemy/enemies.
    RANDOM_TARGET = 0x40  # Bit 6 set.
    NON_RANDOM_TARGET = 0x3F  # Bit 6 not set. Not a proper flag, but used to indicate that all enemies from the specified slots should be shown.

    # Transformation style bitmask (bits 3–0)
    NEO_EXDEATH_APPEARANCE = 0x0D
    MELUSINE_4_APPEARANCE = 0x0C
    MELUSINE_3_APPEARANCE = 0x0B
    MELUSINE_2_APPEARANCE = 0x0A
    MELUSINE_1_APPEARANCE = 0x09
    DIVE_WITH_SOUND = 0x08  # Sandworm
    DIVE_WITHOUT_SOUND = 0x07  # Pages
    FADE_AND_DROP = 0x06  # Unused
    TRANSFORM = 0x05
    SWITCH = 0x04  # Unused
    DROP = 0x03  # Motor Trap
    DISCREET = 0x02
    REPLACE = 0x01  # Iron Claw
    FADE = 0x00

    @classmethod
    def from_mask(cls, mask: int) -> list[TransformationFlags]:
        result: list[TransformationFlags] = []

        # bit 7: HP transfer
        if mask & 0x80:
            result.append(cls.DO_NOT_TRANSFER_HP)
        else:
            result.append(cls.TRANSFER_HP)

        # bit 6: randomness
        if mask & 0x40:
            result.append(cls.RANDOM_TARGET)
        else:
            result.append(cls.NON_RANDOM_TARGET)

        # bits 3–0: transform style (pure value, not a bitmask)
        style_value: int = mask & 0x0F
        result.append(cls(style_value))

        return result

    @override
    def __str__(self) -> str:
        if self == TransformationFlags.DO_NOT_TRANSFER_HP:
            return "Do not transfer HP to the newly shown enemy/enemies"
        elif self == TransformationFlags.TRANSFER_HP:
            return "Transfer HP to the newly shown enemy/enemies"
        elif self == TransformationFlags.RANDOM_TARGET:
            return "Show only a single enemy from a random slot among the specified ones"
        elif self == TransformationFlags.NON_RANDOM_TARGET:
            return "Show all enemies from the specified slots"
        else:
            return f"Style: {self.name.replace("_", " ").capitalize()}"
