from .actions.action import AIRuleAction
from .actions.simple_action import SimpleAction
from .actions.unhide_enemy_action import UnhideEnemyAction
from .actions.set_target_action import SetTargetAction
from .actions.set_variable_action import SetVariableAction
from .actions.unknown_f5_action import UnknownF5Action
from .actions.display_message_action import DisplayMessageAction
from .actions.no_interrupt_action import NoInterruptAction
from .actions.full_screen_effect_action import FullScreenEffectAction
from .actions.set_global_event_flag_action import SetGlobalEventFlagAction
from .actions.set_stats_or_toggle_status_action import SetStatsOrToggleStatusAction
from .actions.gba_random_selection_action import GBARandomSelectionAction
from .actions.random_selection_action import RandomSelectionAction
from .actions.ai_command_action import AICommandAction
from .enums.action_code import ActionCode
from .enums.target import Target
from .enums.variable import Variable
from .enums.global_event_table import GlobalEventTable
from .enums.party_member import PartyMemberParameter


class ActionFactory():
    @staticmethod
    def create_action(bytes: list[int]) -> AIRuleAction:
        if not bytes or len(bytes) < 1:
            raise ValueError("The provided bytes list is empty or None.")
        elif len(bytes) == 1:
            return ActionFactory.__create_simple_action(bytes[0])
        elif len(bytes) == 3:
            return ActionFactory.__create_three_byte_action(bytes)
        elif len(bytes) == 4:
            return ActionFactory.__create_four_byte_action(bytes)
        else:
            raise ValueError("A valid action must be 1, 3, or 4 bytes long.")

    @staticmethod
    def create_no_interrupt_action(sub_actions_cumulative_length: int, third_byte: int, sub_actions_bytes_lists: list[list[int]], length_includes_separator_or_terminator: bool) -> NoInterruptAction:
        if not sub_actions_bytes_lists or len(sub_actions_bytes_lists) < 2:
            raise ValueError("A NoInterruptAction must have at least two sub-actions.")
        
        sub_actions: list[AIRuleAction] = []

        for bytes in sub_actions_bytes_lists:
            sub_action: AIRuleAction = ActionFactory.create_action(bytes)

            sub_actions.append(sub_action)

        return NoInterruptAction(sub_actions_cumulative_length=sub_actions_cumulative_length & 0xFF, third_byte=third_byte & 0xFF, sub_actions=sub_actions, length_includes_separator_or_terminator=length_includes_separator_or_terminator)

    @staticmethod
    def __create_simple_action(action_code: int) -> AIRuleAction:
        return SimpleAction(action_code & 0xFF)

    @staticmethod
    def __create_three_byte_action(bytes: list[int]) -> AIRuleAction:
        action_code: int = bytes[0] & 0xFF
        second_byte: int = bytes[1] & 0xFF
        third_byte: int = bytes[2] & 0xFF

        match ActionCode(action_code):
            case ActionCode.UNHIDE_ENEMY:
                return UnhideEnemyAction(mask=second_byte, enemy_set=third_byte)
            case ActionCode.SET_TARGET:
                return SetTargetAction(target=Target(second_byte), optional_third_byte=third_byte)
            case ActionCode.SET_VARIABLE:
                return SetVariableAction(var_id=Variable(second_byte), value=third_byte)
            case ActionCode.UNKNOWN_F5_ACTION:
                return UnknownF5Action(second_byte=second_byte, third_byte=third_byte)
            case ActionCode.DISPLAY_MESSAGE:
                return DisplayMessageAction(message_table_number=second_byte, message_entry=third_byte)
            case ActionCode.FULL_SCREEN_EFFECT:
                return FullScreenEffectAction(second_byte=second_byte, third_byte=third_byte)
            case ActionCode.SET_GLOBAL_EVENT_FLAG:
                return SetGlobalEventFlagAction(global_event_table_number=GlobalEventTable(second_byte), mask=third_byte)
            case ActionCode.SET_STATS_OR_TOGGLE_STATUS:
                return SetStatsOrToggleStatusAction(parameter=PartyMemberParameter(second_byte), value_msb=third_byte)
            case _:
                raise ValueError(f"Unknown three-byte action code: {action_code:#04x}.")

    @staticmethod
    def __create_four_byte_action(bytes: list[int]) -> AIRuleAction:
        action_code: int = bytes[0] & 0xFF
        second_byte: int = bytes[1] & 0xFF
        third_byte: int = bytes[2] & 0xFF
        fourth_byte: int = bytes[3] & 0xFF

        match ActionCode(action_code):
            case ActionCode.GBA_RANDOM_SELECTION:
                return GBARandomSelectionAction(first_choice=SimpleAction(second_byte), second_choice=SimpleAction(third_byte), third_choice=SimpleAction(fourth_byte))
            case ActionCode.RANDOM_SELECTION:
                return RandomSelectionAction(first_choice=SimpleAction(second_byte), second_choice=SimpleAction(third_byte), third_choice=SimpleAction(fourth_byte))
            case ActionCode.AI_COMMAND:
                return AICommandAction(sub_action=ActionFactory.create_action([second_byte, third_byte, fourth_byte]))
            case _:
                raise ValueError(f"Unknown four-byte action code: {action_code:#04x}.")
