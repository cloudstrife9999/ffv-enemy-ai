from .actions.action import AIRuleAction
from .actions.simple_action import SimpleAction
from .actions.set_enemy_to_show import SetEnemyToShowAction
from .actions.set_target_action import SetTargetAction
from .actions.set_variable_action import SetVariableAction
from .actions.unknown_f5_action import UnknownF5Action
from .actions.display_message_action import DisplayMessageAction
from .actions.no_interrupt_action import NoInterruptAction
from .actions.full_screen_effect_action import FullScreenEffectAction
from .actions.set_global_event_flag_action import SetGlobalEventFlagAction
from .actions.toggle_status_action import ToggleStatusAction
from .actions.gba_random_selection_action import GBARandomSelectionAction
from .actions.random_selection_action import RandomSelectionAction
from .actions.ai_command_action import AICommandAction
from .enums.action_code import ActionCode
from .ability import Ability
from .enums.target import Target
from .enums.variable import Variable
from .enums.global_event_table import GlobalEventTable
from .enums.stats_and_properties_table import StatsAndPropertiesTable


class ActionFactory():
    @staticmethod
    def create_action(bytes: list[int], battle_text: dict[int, dict[int, str]]) -> AIRuleAction:
        if not bytes or len(bytes) < 1:
            raise ValueError("The provided bytes list is empty or None.")
        elif len(bytes) == 1:
            return ActionFactory.__create_simple_action(bytes[0])
        elif len(bytes) == 3:
            return ActionFactory.__create_three_byte_action(bytes, battle_text)
        elif len(bytes) == 4:
            return ActionFactory.__create_four_byte_action(bytes, battle_text)
        else:
            raise ValueError("A valid action must be 1, 3, or 4 bytes long.")

    @staticmethod
    def __create_simple_action(action_code: int) -> AIRuleAction:
        return SimpleAction(action_code & 0xFF)

    @staticmethod
    def __create_three_byte_action(bytes: list[int], battle_text: dict[int, dict[int, str]]) -> AIRuleAction:
        action_code: int = bytes[0] & 0xFF
        second_byte: int = bytes[1] & 0xFF
        third_byte: int = bytes[2] & 0xFF

        match ActionCode(action_code):
            case ActionCode.SET_ENEMY_TO_SHOW:
                return SetEnemyToShowAction(flags=second_byte, slot_mask=third_byte)
            case ActionCode.SET_TARGET:
                return SetTargetAction(target=Target(second_byte), optional_third_byte=third_byte)
            case ActionCode.SET_VARIABLE:
                return SetVariableAction(var_id=Variable(second_byte), value=third_byte)
            case ActionCode.UNKNOWN_F5_ACTION:
                return UnknownF5Action(second_byte=second_byte, third_byte=third_byte)
            case ActionCode.DISPLAY_MESSAGE:
                return DisplayMessageAction(message_table_number=second_byte, message_entry=third_byte, battle_text=battle_text)
            case ActionCode.NO_INTERRUPT:
                return NoInterruptAction(sub_actions_cumulative_length=second_byte, third_byte=third_byte)
            case ActionCode.FULL_SCREEN_EFFECT:
                return FullScreenEffectAction(second_byte=second_byte, third_byte=third_byte)
            case ActionCode.SET_GLOBAL_EVENT_FLAG:
                return SetGlobalEventFlagAction(global_event_table_number=GlobalEventTable(second_byte), mask=third_byte)
            case ActionCode.SET_STATS_OR_TOGGLE_STATUS:
                return ToggleStatusAction(property_table=StatsAndPropertiesTable(second_byte), mask=third_byte)
            case _:
                raise ValueError(f"Unknown three-byte action code: {action_code:#04x}.")

    @staticmethod
    def __create_four_byte_action(bytes: list[int], battle_text: dict[int, dict[int, str]]) -> AIRuleAction:
        action_code: int = bytes[0] & 0xFF
        second_byte: int = bytes[1] & 0xFF
        third_byte: int = bytes[2] & 0xFF
        fourth_byte: int = bytes[3] & 0xFF

        match ActionCode(action_code):
            case ActionCode.GBA_RANDOM_SELECTION:
                return GBARandomSelectionAction(first_choice=SimpleAction(second_byte), second_choice=SimpleAction(third_byte), third_choice=SimpleAction(fourth_byte))
            case ActionCode.RANDOM_SELECTION | ActionCode.AI_COMMAND:
                if all(Ability.is_valid_non_dark_arts_id(byte) for byte in (second_byte, third_byte, fourth_byte)):
                    return RandomSelectionAction(first_choice=SimpleAction(second_byte), second_choice=SimpleAction(third_byte), third_choice=SimpleAction(fourth_byte))
                else:
                    return AICommandAction(sub_action=ActionFactory.create_action([second_byte, third_byte, fourth_byte], battle_text))
            case _:
                raise ValueError(f"Unknown four-byte action code: {action_code:#04x}.")
