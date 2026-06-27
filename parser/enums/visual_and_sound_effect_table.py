from enum import IntEnum
from typing import override


class VisualAndSoundEffectTable(IntEnum):
    CHANGE_MUSIC = 0x00
    PLAY_SOUND_EFFECT = 0x01
    LIGHT_EFFECT = 0x03
    VISUAL_EFFECTS = 0x05  # Unused in the game
    SHAKING_EFFECT = 0x09
    BRIGHTNESS_EFFECT = 0x0A

    @override
    def __str__(self) -> str:
        return f"\"{self.name.title()}\" table"

    @classmethod
    def is_valid_effect_table_id(cls, value: int) -> bool:
        return value in cls._value2member_map_

'''
FD F8 XX YY experiments

XX == 0x02: nothing happens with any follow-up bytes.

XX == 0x04: nothing happens with any follow-up bytes.

XX == 0x05: mask YY with 0x07:
- 00: clears visual effects from this group
- 01: flash (only once until the next 0x00)
- 02: mosaic of alternating colours (permanent until the next 0x00)
- 03: battle background fades to black (only once until the next 0x00)
- 04: night effect (permanent until the next 0x00)
- 05: night effect (permanent until the next 0x00)
- 06: nothing happens
- 07: nothing happens

XX == 0x06: mask YY with 0x07:
- 00: nothing happens
- 01: nothing happens
- 02: nothing happens
- 03: nothing happens
- 04: nothing happens
- 05: waves moving upwards on all enemy sprites (permanent)
- 06: waves moving upwards on the battle background (permanent)
- 07: combination of 05 and 06 (permanent)

XX == 0x07: long or short pause between script and following action, depending on the value of the follow-up byte:
- 0x00: long pause (several seconds)
- 0x01: short pause (less than a second)
- 0x02: short pause (less than a second)
- 0x03: short pause (less than a second)
- 0x04: short pause (less than a second)
- 0x05: short pause (less than a second)
- 0x06: short pause (less than a second)
- 0x07: short pause (less than a second)
- 0x08: short pause (less than a second)
- 0x10: short pause (less than a second)
- 0x20: short pause (less than a second)
- 0x40: short pause (less than a second)
- 0x42: long pause (several seconds)
- 0x80: long pause (several seconds)
- 0x81: long pause (several seconds)
- Other values: untested.

XX == 0x08: mask YY with 0x07:
- 0x00: clears visual effects from this group
- 0x01: dark flash (only once until the next 0x00)
- 0x02: Makes the fading out effect of defeated enemies brighter (permanent until the next 0x00).
- 0x03: Makes the fading out effect of defeated enemies brighter (permanent until the next 0x00).
- 0x04: Makes the fading out effect of defeated enemies brighter (permanent until the next 0x00).
- 0x05: Makes the fading out effect of defeated enemies black (permanent until the next 0x00).
- 0x06: Makes the fading out effect of defeated enemies black (permanent until the next 0x00).
- 0x07: Makes the fading out effect of defeated enemies black (permanent until the next 0x00).
'''