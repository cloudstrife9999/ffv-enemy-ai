from enum import IntEnum
from typing import override


class ActionCode(IntEnum):
    UNHIDE_ENEMY = 0xF2
    SET_TARGET = 0xF3
    SET_VARIABLE = 0xF4
    UNKNOWN_F5_ACTION = 0xF5
    DISPLAY_MESSAGE = 0xF6
    NO_INTERRUPT = 0xF7
    FULL_SCREEN_EFFECT = 0xF8
    SET_GLOBAL_EVENT_FLAG = 0xF9
    SET_STATS_OR_TOGGLE_STATUS = 0xFA
    GBA_RANDOM_SELECTION = 0xFC
    RANDOM_SELECTION = 0xFD
    AI_COMMAND = 0xFD  # Same as RANDOM_SELECTION, but used in a different context.

    @override
    def __str__(self) -> str:
        return self.name.title().replace("_", " ")  # TODO: refine this.
