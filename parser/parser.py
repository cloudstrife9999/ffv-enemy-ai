from typing import Optional

from .state_enum import StateEnum
from .enums.condition_code import ConditionCode
from .enums.target import Target
from .enums.status_table import StatusTable
from .enums.variable import Variable
from .enums.command import Command
from .enums.ability import Ability
from .enums.party_member_offset import PartyMemberPropertyTable
from .enums.global_event_table import GlobalEventTable
from .enums.symbol import SymbolCode
from .enums.action_code import ActionCode


# TODO: rather than simply moving through the states, build a tree of rule objects as we parse the tokens, and add a getter property to return the tree of rule objects.
class StateMachine():
    def __init__(self, tokens: bytes) -> None:
        self.__current_state: StateEnum = StateEnum.START
        self.__tokens: bytes = tokens
        self.__no_interrupt_error_message: str = "Unexpected end of no-interrupt action."

    def parse(self) -> bool:
        return self.__handle_start_state(index_to_read=0)

    def __handle_error_state(self, previous_byte: int, optional_message: Optional[str] = None) -> bool:
        if optional_message:
            print(f"[Parser] Ended up in error state: {optional_message}. Previous byte: 0x{previous_byte:02X} in state {self.__current_state.name}. Tokens: {" ".join(f"{b:02X}" for b in self.__tokens)}.")
        else:
            print(f"[Parser] Ended up in error state: unexpected byte 0x{previous_byte:02X} in state {self.__current_state.name}. Tokens: {" ".join(f"{b:02X}" for b in self.__tokens)}.")

        self.__current_state = StateEnum.ERROR

        return False

    def __handle_start_state(self, index_to_read: int) -> bool:
        '''
        We are in the start state, expecting either of the following:
        - The first byte of a non-default condition (0x01-0x0F).
        - The first byte of a default condition (0x00).
        '''
        self.__current_state = StateEnum.START

        current_byte: int = self.__tokens[index_to_read]

        if not ConditionCode.is_valid_condition_code(current_byte):
            return self.__handle_error_state(previous_byte=current_byte)
        elif ConditionCode(current_byte) is ConditionCode.UNCONDITIONAL:
            return self.__handle_dc1_state(condition_code=ConditionCode(current_byte), index_to_read=index_to_read + 1)
        else:
            return self.__handle_c1_state(condition_code=ConditionCode(current_byte), index_to_read=index_to_read + 1)

    def __handle_c1_state(self, condition_code: ConditionCode, index_to_read: int) -> bool:
        '''
        We just read the first byte of a non-default condition.

        The next byte must be the second byte of a non-default condition.
        '''
        self.__current_state = StateEnum.C1

        current_byte: int = self.__tokens[index_to_read]

        if condition_code.has_irrelevant_second_byte() or condition_code.has_unrestricted_second_byte():
            return self.__handle_c2_state(condition_code=condition_code, index_to_read=index_to_read + 1)
        elif condition_code in (ConditionCode.STATUS_EFFECT, ConditionCode.HP_LOWER_THAN_THRESHOLD, ConditionCode.PARTY_MEMBER_PARAMETER) and Target.is_valid_target_id(current_byte):
            return self.__handle_c2_state(condition_code=condition_code, index_to_read=index_to_read + 1)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_c2_state(self, condition_code: ConditionCode, index_to_read: int) -> bool:
        '''
        We just read the second byte of a non-default condition.

        The next byte must be the third byte of a non-default condition.
        '''
        self.__current_state = StateEnum.C2

        current_byte: int = self.__tokens[index_to_read]

        if condition_code.has_irrelevant_third_byte() or condition_code.has_unrestricted_third_byte():
            return self.__handle_c3_state(condition_code=condition_code, index_to_read=index_to_read + 1)
        elif condition_code is ConditionCode.STATUS_EFFECT and StatusTable.is_valid_status_table_id(current_byte):
            return self.__handle_c3_state(condition_code=condition_code, index_to_read=index_to_read + 1)
        elif condition_code is ConditionCode.VAR_CHECK and Variable.is_valid_var_id(current_byte):
            return self.__handle_c3_state(condition_code=condition_code, index_to_read=index_to_read + 1)
        elif condition_code in (ConditionCode.HIT_BY_COMMAND, ConditionCode.HIT_BY_COMMAND_CLASS) and Command.is_valid_command_id(current_byte):
            return self.__handle_c3_state(condition_code=condition_code, index_to_read=index_to_read + 1)
        elif condition_code is ConditionCode.HIT_BY_SPELL and Ability.is_valid_ability_id(current_byte):
            return self.__handle_c3_state(condition_code=condition_code, index_to_read=index_to_read + 1)
        elif condition_code is ConditionCode.PARTY_MEMBER_PARAMETER and PartyMemberPropertyTable.is_valid_party_member_property_offset(current_byte):
            return self.__handle_c3_state(condition_code=condition_code, index_to_read=index_to_read + 1)
        elif condition_code is ConditionCode.GLOBAL_EVENT_FLAGS and GlobalEventTable.is_valid_global_event_table_id(current_byte):
            return self.__handle_c3_state(condition_code=condition_code, index_to_read=index_to_read + 1)
        else:
            return self.__handle_error_state(previous_byte=current_byte)
            
    def __handle_c3_state(self, condition_code: ConditionCode, index_to_read: int) -> bool:
        '''
        We just read the third byte of a non-default condition.

        The next byte must be the fourth byte of a non-default condition.
        '''
        self.__current_state = StateEnum.C3

        current_byte: int = self.__tokens[index_to_read]

        if condition_code.has_irrelevant_fourth_byte() or condition_code.has_unrestricted_fourth_byte():
            return self.__handle_c4_state(index_to_read=index_to_read + 1)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_c4_state(self, index_to_read: int) -> bool:
        '''
        We just read the fourth byte of a non-default condition.

        The next byte must be either of the following:
        * A separator byte (0xFE) if no more conditions are to be read for this rule.
        * The first byte of a non-default condition (0x01-0x0F) if more conditions are to be read for this rule.
        '''
        self.__current_state = StateEnum.C4

        current_byte: int = self.__tokens[index_to_read]

        if current_byte is SymbolCode.SEPARATOR.value:
            return self.__handle_sep1_state(index_to_read=index_to_read + 1)
        elif ConditionCode.is_valid_condition_code(current_byte):
            return self.__handle_c1_state(condition_code=ConditionCode(current_byte), index_to_read=index_to_read + 1)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_sep1_state(self, index_to_read: int) -> bool:
        '''
        We just read a separator byte (0xFE) after the fourth byte of a non-default condition.

        The next byte must be a simple action byte (0x00-0xEF) or a complex action first byte (0xF2-0xFD).
        '''
        self.__current_state = StateEnum.SEP1

        current_byte: int = self.__tokens[index_to_read]

        if Ability.is_valid_ability_id(current_byte):
            return self.__handle_sa_state(index_to_read=index_to_read + 1, remaining_length=-1)
        elif ActionCode.is_valid_four_byte_action_code(current_byte):
            return self.__handle_ca1_state(action_code=ActionCode(current_byte), index_to_read=index_to_read + 1, remaining_length=-1)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_sa_state(self, index_to_read: int, remaining_length: int) -> bool:
        '''
        We just read a simple action byte (0x00-0xEF).

        The next byte must be one of the following:
        - A separator byte (0xFE), if this is the last action in the action block.
        - A simple action byte (0x00-0xEF).
        - The first byte of a 4-byte GBA random selection action (0xFC).
        - The first byte of a 4-byte SNES random selection action (0xFD).
        - The first byte of a 4-byte AI command (0xFD).

        The two 0xFD cases cannot be disambiguated in the SNES version until the next byte is read.
        '''
        self.__current_state = StateEnum.SA

        remaining_length = max(remaining_length - 1, -1)

        current_byte: int = self.__tokens[index_to_read]

        if current_byte is SymbolCode.SEPARATOR.value and remaining_length != 0:  # A no-interrupt action cannot end here if a separator is read.
            return self.__handle_sep2_state(index_to_read=index_to_read + 1, remaining_length=remaining_length)
        elif current_byte is SymbolCode.SEPARATOR.value and remaining_length == 0:
            return self.__handle_error_state(previous_byte=current_byte, optional_message=self.__no_interrupt_error_message)
        elif Ability.is_valid_ability_id(current_byte):
            return self.__handle_sa_state(index_to_read=index_to_read + 1, remaining_length=remaining_length)
        elif ActionCode.is_valid_four_byte_action_code(current_byte):
            return self.__handle_ca1_state(action_code=ActionCode(current_byte), index_to_read=index_to_read + 1, remaining_length=remaining_length)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_ca1_state(self, action_code: ActionCode, index_to_read: int, remaining_length: int) -> bool:
        '''
        We just read either of the following:
        - The first byte of a 4-byte GBA random selection action (0xFC).
        - The first byte of a 4-byte SNES random selection action (0xFD).
        - The first byte of a 4-byte AI command (0xFD).

        The next byte must be one of the following:
        - A simple action byte (0x00-0xEF) if and only if the previous byte was a 4-byte random selection action (0xFC or 0xFD).
        - A valid 1-byte action code of a 3-byte action (0xF2-0xFA) otherwise (as part of a 4-byte AI command).
        '''
        self.__current_state = StateEnum.CA1

        remaining_length = max(remaining_length - 1, -1)

        current_byte: int = self.__tokens[index_to_read]

        # A no-interrupt action cannot end here.
        if remaining_length == 0:
            return self.__handle_error_state(previous_byte=current_byte, optional_message=self.__no_interrupt_error_message)
        elif action_code in (ActionCode.GBA_RANDOM_SELECTION, ActionCode.RANDOM_SELECTION) and Ability.is_valid_ability_id(current_byte):
            return self.__handle_ca2_state(action_code=action_code, sub_action_code=None, index_to_read=index_to_read + 1, remaining_length=remaining_length)
        elif action_code is ActionCode.AI_COMMAND and ActionCode.is_valid_three_byte_action_code(current_byte):
            return self.__handle_ca2_state(action_code=action_code, sub_action_code=ActionCode(current_byte), index_to_read=index_to_read + 1, remaining_length=remaining_length)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_ca2_state(self, action_code: ActionCode, sub_action_code: Optional[ActionCode], index_to_read: int, remaining_length: int) -> bool:
        '''
        We just read either of the following:
        - A simple action byte (as part of a 4-byte random selection action).
        - A valid 1-byte action code of a 3-byte action (as part of a 4-byte AI command).

        The next byte must be one of the following:
        - A simple action byte (0x00-0xEF) if and only if the previous byte was a simple action byte (as part of a 4-byte random selection action).
        - The second byte of a 3-byte action otherwise (as part of a 4-byte AI command).
        '''
        self.__current_state = StateEnum.CA2

        remaining_length = max(remaining_length - 1, -1)

        current_byte: int = self.__tokens[index_to_read]

        # A no-interrupt action cannot end here.
        if remaining_length == 0:
            return self.__handle_error_state(previous_byte=current_byte, optional_message=self.__no_interrupt_error_message)
        elif action_code in (ActionCode.GBA_RANDOM_SELECTION, ActionCode.RANDOM_SELECTION) and Ability.is_valid_ability_id(current_byte):
            return self.__handle_ca3_state(action_code=action_code, index_to_read=index_to_read + 1, remaining_length=remaining_length)
        elif action_code is not ActionCode.AI_COMMAND:
            return self.__handle_error_state(previous_byte=current_byte)
        else:
            return self.__handle_ca2_state_helper(action_code=action_code, sub_action_code=sub_action_code, current_byte=current_byte, index_to_read=index_to_read, remaining_length=remaining_length)

    def __handle_ca2_state_helper(self, action_code: ActionCode, sub_action_code: Optional[ActionCode], current_byte: int, index_to_read: int, remaining_length: int) -> bool:
        if sub_action_code in (ActionCode.UNHIDE_ENEMY, ActionCode.UNKNOWN_F5_ACTION, ActionCode.DISPLAY_MESSAGE, ActionCode.FULL_SCREEN_EFFECT):
            return self.__handle_ca3_state(action_code=action_code, index_to_read=index_to_read + 1, remaining_length=remaining_length)
        elif sub_action_code is ActionCode.SET_TARGET and Target.is_valid_target_id(current_byte):
            return self.__handle_ca3_state(action_code=action_code, index_to_read=index_to_read + 1, remaining_length=remaining_length)
        elif sub_action_code is ActionCode.SET_VARIABLE and Variable.is_valid_var_id(current_byte):
            return self.__handle_ca3_state(action_code=action_code, index_to_read=index_to_read + 1, remaining_length=remaining_length)
        elif sub_action_code is ActionCode.NO_INTERRUPT and current_byte >= 2:  # The minimum length is the size of 2 simple actions (1 byte each).
            # +1 because the next byte is not covered by the declared length of a no-interrupt action.
            return self.__handle_ca3_state(action_code=action_code, index_to_read=index_to_read + 1, remaining_length=current_byte + 1)
        elif sub_action_code is ActionCode.SET_GLOBAL_EVENT_FLAG and GlobalEventTable.is_valid_global_event_table_id(current_byte):
            return self.__handle_ca3_state(action_code=action_code, index_to_read=index_to_read + 1, remaining_length=remaining_length)
        elif sub_action_code is ActionCode.SET_STATS_OR_TOGGLE_STATUS and PartyMemberPropertyTable.is_valid_party_member_property_offset(current_byte):
            return self.__handle_ca3_state(action_code=action_code, index_to_read=index_to_read + 1, remaining_length=remaining_length)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_ca3_state(self, action_code: ActionCode, index_to_read: int, remaining_length: int) -> bool:
        '''
        We just read either of the following:
        - A simple action byte (as part of a 4-byte random selection action).
        - The second byte of a 3-byte action (as part of a 4-byte AI command).

        The next byte must be one of the following:
        - A simple action byte (0x00-0xEF) if and only if the previous byte was a simple action byte (as part of a 4-byte random selection action).
        - The third byte of a 3-byte action otherwise (as part of a 4-byte AI command).
        '''
        self.__current_state = StateEnum.CA3

        remaining_length = max(remaining_length - 1, -1)

        current_byte: int = self.__tokens[index_to_read]

        # A no-interrupt action cannot end here.
        if remaining_length == 0:
            return self.__handle_error_state(previous_byte=current_byte, optional_message=self.__no_interrupt_error_message)
        elif action_code in (ActionCode.GBA_RANDOM_SELECTION, ActionCode.RANDOM_SELECTION) and Ability.is_valid_ability_id(current_byte):
            return self.__handle_ca4_state(index_to_read=index_to_read + 1, remaining_length=remaining_length)
        elif action_code is ActionCode.AI_COMMAND:  # The last byte is unrestricted for 3-byte actions (as part of a 4-byte command).
            return self.__handle_ca4_state(index_to_read=index_to_read + 1, remaining_length=remaining_length)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_ca4_state(self, index_to_read: int, remaining_length: int) -> bool:
        '''
        We just read either of the following:
        - A simple action byte (as part of a 4-byte random selection action).
        - The third byte of a 3-byte action (as part of a 4-byte AI command).

        The next byte must be one of the following:
        - A separator byte (0xFE), if this is the last action in the action block.
        - A simple action byte (0x00-0xEF).
        - The first byte of a 4-byte GBA random selection action (0xFC).
        - The first byte of a 4-byte SNES random selection action (0xFD).
        - The first byte of a 4-byte AI command (0xFD).

        The two 0xFD cases cannot be disambiguated in the SNES version until the next byte is read.
        '''
        self.__current_state = StateEnum.CA4

        remaining_length = max(remaining_length - 1, -1)

        current_byte: int = self.__tokens[index_to_read]

        if Ability.is_valid_ability_id(current_byte):
            return self.__handle_sa_state(index_to_read=index_to_read + 1, remaining_length=remaining_length)
        elif ActionCode.is_valid_four_byte_action_code(current_byte):
            return self.__handle_ca1_state(action_code=ActionCode(current_byte), index_to_read=index_to_read + 1, remaining_length=remaining_length)
        elif current_byte is SymbolCode.SEPARATOR.value and remaining_length != 0:  # A no-interrupt action cannot end here if a separator is read.
            return self.__handle_sep2_state(index_to_read=index_to_read + 1, remaining_length=remaining_length)
        elif current_byte is SymbolCode.SEPARATOR.value and remaining_length == 0:
            return self.__handle_error_state(previous_byte=current_byte, optional_message=self.__no_interrupt_error_message)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_sep2_state(self, index_to_read: int, remaining_length: int) -> bool:
        '''
        We just read a separator byte (0xFE) after a non-default action block in the active AI.

        The next byte must be either of the following:
        - The first byte of a default condition (0x00), if there are no more non-default rules in the active AI.
        - The first byte of a non-default condition (0x01-0x0F) otherwise.
        '''
        self.__current_state = StateEnum.SEP2

        remaining_length = max(remaining_length - 1, -1)

        current_byte: int = self.__tokens[index_to_read]

        if current_byte is ConditionCode.UNCONDITIONAL.value:
            return self.__handle_dc1_state(condition_code=ConditionCode.UNCONDITIONAL, index_to_read=index_to_read + 1)
        elif ConditionCode.is_valid_condition_code(current_byte):
            return self.__handle_c1_state(condition_code=ConditionCode(current_byte), index_to_read=index_to_read + 1) 
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_dc1_state(self, condition_code: ConditionCode, index_to_read: int) -> bool:
        '''
        We just read the first byte of a default condition.

        The next byte must be the second byte of a default condition.
        '''
        self.__current_state = StateEnum.DC1

        current_byte: int = self.__tokens[index_to_read]

        if condition_code.has_irrelevant_second_byte() or condition_code.has_unrestricted_second_byte():
            return self.__handle_dc2_state(condition_code=condition_code, index_to_read=index_to_read + 1)
        elif condition_code in (ConditionCode.STATUS_EFFECT, ConditionCode.HP_LOWER_THAN_THRESHOLD, ConditionCode.PARTY_MEMBER_PARAMETER) and Target.is_valid_target_id(current_byte):
            return self.__handle_dc2_state(condition_code=condition_code, index_to_read=index_to_read + 1)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_dc2_state(self, condition_code: ConditionCode, index_to_read: int) -> bool:
        '''
        We just read the second byte of a default condition.

        The next byte must be the third byte of a default condition.
        '''
        self.__current_state = StateEnum.DC2

        current_byte: int = self.__tokens[index_to_read]

        if condition_code.has_irrelevant_third_byte() or condition_code.has_unrestricted_third_byte():
            return self.__handle_dc3_state(condition_code=condition_code, index_to_read=index_to_read + 1)
        elif condition_code is ConditionCode.STATUS_EFFECT and StatusTable.is_valid_status_table_id(current_byte):
            return self.__handle_dc3_state(condition_code=condition_code, index_to_read=index_to_read + 1)
        elif condition_code is ConditionCode.VAR_CHECK and Variable.is_valid_var_id(current_byte):
            return self.__handle_dc3_state(condition_code=condition_code, index_to_read=index_to_read + 1)
        elif condition_code in (ConditionCode.HIT_BY_COMMAND, ConditionCode.HIT_BY_COMMAND_CLASS) and Command.is_valid_command_id(current_byte):
            return self.__handle_dc3_state(condition_code=condition_code, index_to_read=index_to_read + 1)
        elif condition_code is ConditionCode.HIT_BY_SPELL and Ability.is_valid_ability_id(current_byte):
            return self.__handle_dc3_state(condition_code=condition_code, index_to_read=index_to_read + 1)
        elif condition_code is ConditionCode.PARTY_MEMBER_PARAMETER and PartyMemberPropertyTable.is_valid_party_member_property_offset(current_byte):
            return self.__handle_dc3_state(condition_code=condition_code, index_to_read=index_to_read + 1)
        elif condition_code is ConditionCode.GLOBAL_EVENT_FLAGS and GlobalEventTable.is_valid_global_event_table_id(current_byte):
            return self.__handle_dc3_state(condition_code=condition_code, index_to_read=index_to_read + 1)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_dc3_state(self, condition_code: ConditionCode, index_to_read: int) -> bool:
        '''
        We just read the third byte of a default condition.

        The next byte must be the fourth byte of a default condition.
        '''
        self.__current_state = StateEnum.DC3

        current_byte: int = self.__tokens[index_to_read]

        if condition_code.has_irrelevant_fourth_byte() or condition_code.has_unrestricted_fourth_byte():
            return self.__handle_dc4_state(index_to_read=index_to_read + 1)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_dc4_state(self, index_to_read: int) -> bool:
        '''
        We just read the fourth byte of a default condition.

        The next byte must be a separator byte (0xFE), as the default condition cannot be in AND with any other conditions (default or non-default).
        '''
        self.__current_state = StateEnum.DC4

        current_byte: int = self.__tokens[index_to_read]

        if current_byte is SymbolCode.SEPARATOR.value:
            return self.__handle_sep3_state(index_to_read=index_to_read + 1)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_sep3_state(self, index_to_read: int) -> bool:
        '''
        We just read a separator byte (0xFE) after the fourth byte of a default condition.

        The next byte must be a simple action byte (0x00-0xEF) or a complex action first byte (0xF2-0xFD).
        '''
        self.__current_state = StateEnum.SEP3

        current_byte: int = self.__tokens[index_to_read]

        if Ability.is_valid_ability_id(current_byte):
            return self.__handle_sda_state(index_to_read=index_to_read + 1, remaining_length=-1)
        elif ActionCode.is_valid_four_byte_action_code(current_byte):
            return self.__handle_cda1_state(action_code=ActionCode(current_byte), index_to_read=index_to_read + 1, remaining_length=-1)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_sda_state(self, index_to_read: int, remaining_length: int) -> bool:
        '''
        We just read a simple action byte (0x00-0xEF).

        The next byte must be one of the following:
        - A terminator byte (0xFF), if this is the last action in the default action block (and in the active AI as well).
        - A simple action byte (0x00-0xEF).
        - The first byte of a 4-byte GBA random selection action (0xFC).
        - The first byte of a 4-byte SNES random selection action (0xFD).
        - The first byte of a 4-byte AI command action (0xFD).

        The two 0xFD cases cannot be disambiguated in the SNES version until the next byte is read.
        '''
        self.__current_state = StateEnum.SDA

        remaining_length = max(remaining_length - 1, -1)

        current_byte: int = self.__tokens[index_to_read]

        if current_byte is SymbolCode.TERMINATOR.value and remaining_length != 0:  # A no-interrupt action cannot end here if a terminator is read.
            return self.__handle_ter1_state(index_to_read=index_to_read + 1, remaining_length=remaining_length)
        elif current_byte is SymbolCode.TERMINATOR.value and remaining_length == 0:
            return self.__handle_error_state(previous_byte=current_byte, optional_message=self.__no_interrupt_error_message)
        elif Ability.is_valid_ability_id(current_byte):
            return self.__handle_sda_state(index_to_read=index_to_read + 1, remaining_length=remaining_length)
        elif ActionCode.is_valid_four_byte_action_code(current_byte):
            return self.__handle_cda1_state(action_code=ActionCode(current_byte), index_to_read=index_to_read + 1, remaining_length=remaining_length)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_cda1_state(self, action_code: ActionCode, index_to_read: int, remaining_length: int) -> bool:
        '''
        We just read either of the following:
        - The first byte of a 4-byte GBA random selection action (0xFC).
        - The first byte of a 4-byte SNES random selection action (0xFD).
        - The first byte of a 4-byte AI command action (0xFD).

        The next byte must be one of the following:
        - A simple action byte (0x00-0xEF) if and only if the previous byte was a 4-byte random selection action (0xFC or 0xFD).
        - A valid 1-byte action code of a 3-byte action (0xF2-0xFA) otherwise (as part of a 4-byte AI command action).
        '''
        self.__current_state = StateEnum.CDA1

        remaining_length = max(remaining_length - 1, -1)

        current_byte: int = self.__tokens[index_to_read]

        # A no-interrupt action cannot end here.
        if remaining_length == 0:
            return self.__handle_error_state(previous_byte=current_byte, optional_message=self.__no_interrupt_error_message)

        if action_code in (ActionCode.GBA_RANDOM_SELECTION, ActionCode.RANDOM_SELECTION) and Ability.is_valid_ability_id(current_byte):
            return self.__handle_cda2_state(action_code=action_code, sub_action_code=None, index_to_read=index_to_read + 1, remaining_length=remaining_length)
        elif action_code is ActionCode.AI_COMMAND and ActionCode.is_valid_three_byte_action_code(current_byte):
            return self.__handle_cda2_state(action_code=action_code, sub_action_code=ActionCode(current_byte), index_to_read=index_to_read + 1, remaining_length=remaining_length)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_cda2_state(self, action_code: ActionCode, sub_action_code: Optional[ActionCode], index_to_read: int, remaining_length: int) -> bool:
        '''
        We just read either of the following:
        - A simple action byte (as part of a 4-byte random selection action).
        - A valid 1-byte action code of a 3-byte action (as part of a 4-byte AI command action).

        The next byte must be one of the following:
        - A simple action byte (0x00-0xEF) if and only if the previous byte was a simple action byte (as part of a 4-byte random selection action).
        - The second byte of a 3-byte action otherwise (as part of a 4-byte AI command action).
        '''
        self.__current_state = StateEnum.CDA2

        remaining_length = max(remaining_length - 1, -1)

        current_byte: int = self.__tokens[index_to_read]

        # A no-interrupt action cannot end here.
        if remaining_length == 0:
            return self.__handle_error_state(previous_byte=current_byte, optional_message=self.__no_interrupt_error_message)
        elif action_code in (ActionCode.GBA_RANDOM_SELECTION, ActionCode.RANDOM_SELECTION) and Ability.is_valid_ability_id(current_byte):
            return self.__handle_cda3_state(action_code=action_code, index_to_read=index_to_read + 1, remaining_length=remaining_length)
        elif action_code is not ActionCode.AI_COMMAND:
            return self.__handle_error_state(previous_byte=current_byte)
        else:
            return self.__handle_cda2_state_helper(action_code=action_code, sub_action_code=sub_action_code, current_byte=current_byte, index_to_read=index_to_read, remaining_length=remaining_length)

    def __handle_cda2_state_helper(self, action_code: ActionCode, sub_action_code: Optional[ActionCode], current_byte: int, index_to_read: int, remaining_length: int) -> bool:
        if sub_action_code in (ActionCode.UNHIDE_ENEMY, ActionCode.UNKNOWN_F5_ACTION, ActionCode.DISPLAY_MESSAGE, ActionCode.FULL_SCREEN_EFFECT):
            return self.__handle_cda3_state(action_code=action_code, index_to_read=index_to_read + 1, remaining_length=remaining_length)
        elif sub_action_code is ActionCode.SET_TARGET and Target.is_valid_target_id(current_byte):
            return self.__handle_cda3_state(action_code=action_code, index_to_read=index_to_read + 1, remaining_length=remaining_length)
        elif sub_action_code is ActionCode.SET_VARIABLE and Variable.is_valid_var_id(current_byte):
            return self.__handle_cda3_state(action_code=action_code, index_to_read=index_to_read + 1, remaining_length=remaining_length)
        elif sub_action_code is ActionCode.NO_INTERRUPT and current_byte >= 2:  # The minimum length is the size of 2 simple actions (1 byte each).
            # +1 because the next byte is not covered by the declared length of a no-interrupt action.
            return self.__handle_cda3_state(action_code=action_code, index_to_read=index_to_read + 1, remaining_length=current_byte + 1)
        elif sub_action_code is ActionCode.SET_GLOBAL_EVENT_FLAG and GlobalEventTable.is_valid_global_event_table_id(current_byte):
            return self.__handle_cda3_state(action_code=action_code, index_to_read=index_to_read + 1, remaining_length=remaining_length)
        elif sub_action_code is ActionCode.SET_STATS_OR_TOGGLE_STATUS and PartyMemberPropertyTable.is_valid_party_member_property_offset(current_byte):
            return self.__handle_cda3_state(action_code=action_code, index_to_read=index_to_read + 1, remaining_length=remaining_length)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_cda3_state(self, action_code: ActionCode, index_to_read: int, remaining_length: int) -> bool:
        '''
        We just read either of the following:
        - A simple action byte (as part of a 4-byte random selection action).
        - The second byte of a 3-byte action (as part of a 4-byte AI command action).

        The next byte must be one of the following:
        - A simple action byte (0x00-0xEF) if and only if the previous byte was a simple action byte (as part of a 4-byte random selection action).
        - The third byte of a 3-byte action otherwise (as part of a 4-byte AI command action).
        '''
        self.__current_state = StateEnum.CDA3

        remaining_length = max(remaining_length - 1, -1)

        current_byte: int = self.__tokens[index_to_read]

        # A no-interrupt action cannot end here.
        if remaining_length == 0:
            return self.__handle_error_state(previous_byte=current_byte, optional_message=self.__no_interrupt_error_message)
        elif action_code in (ActionCode.GBA_RANDOM_SELECTION, ActionCode.RANDOM_SELECTION) and Ability.is_valid_ability_id(current_byte):
            return self.__handle_cda4_state(index_to_read=index_to_read + 1, remaining_length=remaining_length)
        elif action_code is ActionCode.AI_COMMAND:  # The last byte is unrestricted for 3-byte actions (as part of a 4-byte command).
            return self.__handle_cda4_state(index_to_read=index_to_read + 1, remaining_length=remaining_length)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_cda4_state(self, index_to_read: int, remaining_length: int) -> bool:
        '''
        We just read either of the following:
        - A simple action byte (as part of a 4-byte random selection action).
        - The third byte of a 3-byte action (as part of a 4-byte AI command action).

        The next byte must be one of the following:
        - A terminator byte (0xFF), if this is the last action in the action block (and in the active AI as well).
        - A simple action byte (0x00-0xEF).
        - The first byte of a 4-byte GBA random selection action (0xFC).
        - The first byte of a 4-byte SNES random selection action (0xFD).
        - The first byte of a 4-byte AI command action (0xFD).

        The two 0xFD cases cannot be disambiguated in the SNES version until the next byte is read.
        '''
        self.__current_state = StateEnum.CDA4

        remaining_length = max(remaining_length - 1, -1)

        current_byte: int = self.__tokens[index_to_read]

        if Ability.is_valid_ability_id(current_byte):
            return self.__handle_sda_state(index_to_read=index_to_read + 1, remaining_length=remaining_length)
        elif ActionCode.is_valid_four_byte_action_code(current_byte):
            return self.__handle_cda1_state(action_code=ActionCode(current_byte), index_to_read=index_to_read + 1, remaining_length=remaining_length)
        elif current_byte is SymbolCode.TERMINATOR.value and remaining_length != 0:  # A no-interrupt action cannot end here if a terminator is read.
            return self.__handle_ter1_state(index_to_read=index_to_read + 1, remaining_length=remaining_length)
        elif current_byte is SymbolCode.TERMINATOR.value and remaining_length == 0:
            return self.__handle_error_state(previous_byte=current_byte, optional_message=self.__no_interrupt_error_message)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_ter1_state(self, index_to_read: int, remaining_length: int) -> bool:
        '''
        We just read a terminator byte (0xFF) after the last action in the default action block (and in the active AI as well).

        The next byte must be either of the following:
        - Another terminator byte (0xFF), if the reactive AI is empty.
        - The first byte of a reactive condition (0x01-0x0F) otherwise.
        '''
        self.__current_state = StateEnum.TER1

        remaining_length = max(remaining_length - 1, -1)

        current_byte: int = self.__tokens[index_to_read]

        if current_byte is SymbolCode.TERMINATOR.value:
            return self.__handle_ter2_state(previous_byte=current_byte, index_to_read=index_to_read + 1, remaining_length=remaining_length)
        elif ConditionCode.is_valid_condition_code(current_byte) and current_byte is not ConditionCode.UNCONDITIONAL.value:
            return self.__handle_rc1_state(condition_code=ConditionCode(current_byte), index_to_read=index_to_read + 1)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_rc1_state(self, condition_code: ConditionCode, index_to_read: int) -> bool:
        '''
        We just read the first byte of a reactive condition in the reactive AI.

        The next byte must be the second byte of a reactive condition.
        '''
        self.__current_state = StateEnum.RC1

        current_byte: int = self.__tokens[index_to_read]

        if condition_code.has_irrelevant_second_byte() or condition_code.has_unrestricted_second_byte():
            return self.__handle_rc2_state(condition_code=condition_code, index_to_read=index_to_read + 1)
        elif condition_code in (ConditionCode.STATUS_EFFECT, ConditionCode.HP_LOWER_THAN_THRESHOLD, ConditionCode.PARTY_MEMBER_PARAMETER) and Target.is_valid_target_id(current_byte):
            return self.__handle_rc2_state(condition_code=condition_code, index_to_read=index_to_read + 1)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_rc2_state(self, condition_code: ConditionCode, index_to_read: int) -> bool:
        '''
        We just read the second byte of a reactive condition in the reactive AI.

        The next byte must be the third byte of a reactive condition.
        '''
        self.__current_state = StateEnum.RC2

        current_byte: int = self.__tokens[index_to_read]

        if condition_code.has_irrelevant_third_byte() or condition_code.has_unrestricted_third_byte():
            return self.__handle_rc3_state(condition_code=condition_code, index_to_read=index_to_read + 1)
        elif condition_code is ConditionCode.STATUS_EFFECT and StatusTable.is_valid_status_table_id(current_byte):
            return self.__handle_rc3_state(condition_code=condition_code, index_to_read=index_to_read + 1)
        elif condition_code is ConditionCode.VAR_CHECK and Variable.is_valid_var_id(current_byte):
            return self.__handle_rc3_state(condition_code=condition_code, index_to_read=index_to_read + 1)
        elif condition_code in (ConditionCode.HIT_BY_COMMAND, ConditionCode.HIT_BY_COMMAND_CLASS) and Command.is_valid_command_id(current_byte):
            return self.__handle_rc3_state(condition_code=condition_code, index_to_read=index_to_read + 1)
        elif condition_code is ConditionCode.HIT_BY_SPELL and Ability.is_valid_ability_id(current_byte):
            return self.__handle_rc3_state(condition_code=condition_code, index_to_read=index_to_read + 1)
        elif condition_code is ConditionCode.PARTY_MEMBER_PARAMETER and PartyMemberPropertyTable.is_valid_party_member_property_offset(current_byte):
            return self.__handle_rc3_state(condition_code=condition_code, index_to_read=index_to_read + 1)
        elif condition_code is ConditionCode.GLOBAL_EVENT_FLAGS and GlobalEventTable.is_valid_global_event_table_id(current_byte):
            return self.__handle_rc3_state(condition_code=condition_code, index_to_read=index_to_read + 1)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_rc3_state(self, condition_code: ConditionCode, index_to_read: int) -> bool:
        '''
        We just read the third byte of a reactive condition in the reactive AI.

        The next byte must be the fourth byte of a reactive condition.
        '''
        self.__current_state = StateEnum.RC3

        current_byte: int = self.__tokens[index_to_read]

        if condition_code.has_irrelevant_fourth_byte() or condition_code.has_unrestricted_fourth_byte():
            return self.__handle_rc4_state(index_to_read=index_to_read + 1)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_rc4_state(self, index_to_read: int) -> bool:
        '''
        We just read the fourth byte of a reactive condition in the reactive AI.

        The next byte must be either of the following:
        * A separator byte (0xFE) if no more conditions are to be read for this rule.
        * The first byte of a reactive condition (0x01-0x0F) if more conditions are to be read for this rule.
        '''
        self.__current_state = StateEnum.RC4

        current_byte: int = self.__tokens[index_to_read]

        if current_byte is SymbolCode.SEPARATOR.value:
            return self.__handle_sep4_state(index_to_read=index_to_read + 1)
        elif ConditionCode.is_valid_condition_code(current_byte):
            return self.__handle_rc1_state(condition_code=ConditionCode(current_byte), index_to_read=index_to_read + 1)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_sep4_state(self, index_to_read: int) -> bool:
        '''
        We just read a separator byte (0xFE) after the fourth byte of a reactive condition.

        The next byte must be a simple action byte (0x00-0xEF) or a complex action first byte (0xF2-0xFD).
        '''
        self.__current_state = StateEnum.SEP4

        current_byte: int = self.__tokens[index_to_read]

        if Ability.is_valid_ability_id(current_byte):
            return self.__handle_rsa_state(index_to_read=index_to_read + 1, remaining_length=-1)
        elif ActionCode.is_valid_four_byte_action_code(current_byte):
            return self.__handle_rca1_state(action_code=ActionCode(current_byte), index_to_read=index_to_read + 1, remaining_length=-1)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_rsa_state(self, index_to_read: int, remaining_length: int) -> bool:
        '''
        We just read a simple action byte (0x00-0xEF).

        The next byte must be one of the following:
        - A separator byte (0xFE), if this is the last action in the action block, but there are more rules in the reactive AI.
        - A terminator byte (0xFF), if the reactive AI has no more rules.
        - A simple action byte (0x00-0xEF).
        - The first byte of a 4-byte GBA random selection action (0xFC).
        - The first byte of a 4-byte SNES random selection action (0xFD).
        - The first byte of a 4-byte AI command (0xFD).

        The two 0xFD cases cannot be disambiguated in the SNES version until the next byte is read.
        '''
        self.__current_state = StateEnum.RSA

        remaining_length = max(remaining_length - 1, -1)

        current_byte: int = self.__tokens[index_to_read]

        if current_byte is SymbolCode.SEPARATOR.value and remaining_length != 0:  # A no-interrupt action cannot end here if a separator is read.
            return self.__handle_sep5_state(index_to_read=index_to_read + 1, remaining_length=remaining_length)
        elif current_byte is SymbolCode.TERMINATOR.value and remaining_length != 0:  # A no-interrupt action cannot end here if a terminator is read.
            return self.__handle_ter2_state(previous_byte=current_byte, index_to_read=index_to_read + 1, remaining_length=remaining_length)
        elif current_byte in (SymbolCode.SEPARATOR.value, SymbolCode.TERMINATOR.value) and remaining_length == 0:
            return self.__handle_error_state(previous_byte=current_byte, optional_message=self.__no_interrupt_error_message)
        elif Ability.is_valid_ability_id(current_byte):
            return self.__handle_rsa_state(index_to_read=index_to_read + 1, remaining_length=remaining_length)
        elif ActionCode.is_valid_four_byte_action_code(current_byte):
            return self.__handle_rca1_state(action_code=ActionCode(current_byte), index_to_read=index_to_read + 1, remaining_length=remaining_length)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_rca1_state(self, action_code: ActionCode, index_to_read: int, remaining_length: int) -> bool:
        '''
        We just read either of the following:
        - The first byte of a 4-byte GBA random selection action (0xFC).
        - The first byte of a 4-byte SNES random selection action (0xFD).
        - The first byte of a 4-byte AI command (0xFD).

        The next byte must be one of the following:
        - A simple action byte (0x00-0xEF) if and only if the previous byte was a 4-byte random selection action (0xFC or 0xFD).
        - A valid 1-byte action code of a 3-byte action (0xF2-0xFA) otherwise (as part of a 4-byte AI command).
        '''
        self.__current_state = StateEnum.RCA1

        remaining_length = max(remaining_length - 1, -1)

        current_byte: int = self.__tokens[index_to_read]

        # A no-interrupt action cannot end here.
        if remaining_length == 0:
            return self.__handle_error_state(previous_byte=current_byte, optional_message=self.__no_interrupt_error_message)
        elif action_code in (ActionCode.GBA_RANDOM_SELECTION, ActionCode.RANDOM_SELECTION) and Ability.is_valid_ability_id(current_byte):
            return self.__handle_rca2_state(action_code=action_code, sub_action_code=None, index_to_read=index_to_read + 1, remaining_length=remaining_length)
        elif action_code is ActionCode.AI_COMMAND and ActionCode.is_valid_three_byte_action_code(current_byte):
            return self.__handle_rca2_state(action_code=action_code, sub_action_code=ActionCode(current_byte), index_to_read=index_to_read + 1, remaining_length=remaining_length)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_rca2_state(self, action_code: ActionCode, sub_action_code: Optional[ActionCode], index_to_read: int, remaining_length: int) -> bool:
        '''
        We just read either of the following:
        - A simple action byte (as part of a 4-byte random selection action).
        - A valid 1-byte action code of a 3-byte action (as part of a 4-byte AI command).

        The next byte must be one of the following:
        - A simple action byte (0x00-0xEF) if and only if the previous byte was a simple action byte (as part of a 4-byte random selection action).
        - The second byte of a 3-byte action otherwise (as part of a 4-byte AI command).
        '''
        self.__current_state = StateEnum.RCA2

        remaining_length = max(remaining_length - 1, -1)

        current_byte: int = self.__tokens[index_to_read]

        # A no-interrupt action cannot end here.
        if remaining_length == 0:
            return self.__handle_error_state(previous_byte=current_byte, optional_message=self.__no_interrupt_error_message)
        elif action_code in (ActionCode.GBA_RANDOM_SELECTION, ActionCode.RANDOM_SELECTION) and Ability.is_valid_ability_id(current_byte):
            return self.__handle_rca3_state(action_code=action_code, index_to_read=index_to_read + 1, remaining_length=remaining_length)
        elif action_code is not ActionCode.AI_COMMAND:
            return self.__handle_error_state(previous_byte=current_byte)
        else:
            return self.__handle_rca2_state_helper(action_code=action_code, sub_action_code=sub_action_code, current_byte=current_byte, index_to_read=index_to_read, remaining_length=remaining_length)

    def __handle_rca2_state_helper(self, action_code: ActionCode, sub_action_code: Optional[ActionCode], current_byte: int, index_to_read: int, remaining_length: int) -> bool:
        if sub_action_code in (ActionCode.UNHIDE_ENEMY, ActionCode.UNKNOWN_F5_ACTION, ActionCode.DISPLAY_MESSAGE, ActionCode.FULL_SCREEN_EFFECT):
            return self.__handle_rca3_state(action_code=action_code, index_to_read=index_to_read + 1, remaining_length=remaining_length)
        elif sub_action_code is ActionCode.SET_TARGET and Target.is_valid_target_id(current_byte):
            return self.__handle_rca3_state(action_code=action_code, index_to_read=index_to_read + 1, remaining_length=remaining_length)
        elif sub_action_code is ActionCode.SET_VARIABLE and Variable.is_valid_var_id(current_byte):
            return self.__handle_rca3_state(action_code=action_code, index_to_read=index_to_read + 1, remaining_length=remaining_length)
        elif sub_action_code is ActionCode.NO_INTERRUPT and current_byte >= 2:  # The minimum length is the size of 2 simple actions (1 byte each).
            # +1 because the next byte is not covered by the declared length of a no-interrupt action.
            return self.__handle_rca3_state(action_code=action_code, index_to_read=index_to_read + 1, remaining_length=current_byte + 1)
        elif sub_action_code is ActionCode.SET_GLOBAL_EVENT_FLAG and GlobalEventTable.is_valid_global_event_table_id(current_byte):
            return self.__handle_rca3_state(action_code=action_code, index_to_read=index_to_read + 1, remaining_length=remaining_length)
        elif sub_action_code is ActionCode.SET_STATS_OR_TOGGLE_STATUS and PartyMemberPropertyTable.is_valid_party_member_property_offset(current_byte):
            return self.__handle_rca3_state(action_code=action_code, index_to_read=index_to_read + 1, remaining_length=remaining_length)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_rca3_state(self, action_code: ActionCode, index_to_read: int, remaining_length: int) -> bool:
        '''
        We just read either of the following:
        - A simple action byte (as part of a 4-byte random selection action).
        - The second byte of a 3-byte action (as part of a 4-byte AI command).

        The next byte must be one of the following:
        - A simple action byte (0x00-0xEF) if and only if the previous byte was a simple action byte (as part of a 4-byte random selection action).
        - The third byte of a 3-byte action otherwise (as part of a 4-byte AI command).
        '''
        self.__current_state = StateEnum.RCA3

        remaining_length = max(remaining_length - 1, -1)

        current_byte: int = self.__tokens[index_to_read]

        # A no-interrupt action cannot end here.
        if remaining_length == 0:
            return self.__handle_error_state(previous_byte=current_byte, optional_message=self.__no_interrupt_error_message)
        elif action_code in (ActionCode.GBA_RANDOM_SELECTION, ActionCode.RANDOM_SELECTION) and Ability.is_valid_ability_id(current_byte):
            return self.__handle_rca4_state(index_to_read=index_to_read + 1, remaining_length=remaining_length)
        elif action_code is ActionCode.AI_COMMAND:  # The last byte is unrestricted for 3-byte actions (as part of a 4-byte command).
            return self.__handle_rca4_state(index_to_read=index_to_read + 1, remaining_length=remaining_length)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_rca4_state(self, index_to_read: int, remaining_length: int) -> bool:
        '''
        We just read either of the following:
        - A simple action byte (as part of a 4-byte random selection action).
        - The third byte of a 3-byte action (as part of a 4-byte AI command).

        The next byte must be one of the following:
        - A separator byte (0xFE), if this is the last action in the action block, but there are more rules in the reactive AI.
        - A terminator byte (0xFF), if the reactive AI has no more rules.
        - A simple action byte (0x00-0xEF).
        - The first byte of a 4-byte GBA random selection action (0xFC).
        - The first byte of a 4-byte SNES random selection action (0xFD).
        - The first byte of a 4-byte AI command (0xFD).

        The two 0xFD cases cannot be disambiguated in the SNES version until the next byte is read.
        '''
        self.__current_state = StateEnum.RCA4

        remaining_length = max(remaining_length - 1, -1)

        current_byte: int = self.__tokens[index_to_read]

        if Ability.is_valid_ability_id(current_byte):
            return self.__handle_rsa_state(index_to_read=index_to_read + 1, remaining_length=remaining_length)
        elif ActionCode.is_valid_four_byte_action_code(current_byte):
            return self.__handle_rca1_state(action_code=ActionCode(current_byte), index_to_read=index_to_read + 1, remaining_length=remaining_length)
        elif current_byte is SymbolCode.SEPARATOR.value and remaining_length != 0:  # A no-interrupt action cannot end here if a separator is read.
            return self.__handle_sep5_state(index_to_read=index_to_read + 1, remaining_length=remaining_length)
        elif current_byte is SymbolCode.TERMINATOR.value and remaining_length != 0:  # A no-interrupt action cannot end here if a terminator is read.
            return self.__handle_ter2_state(previous_byte=current_byte, index_to_read=index_to_read + 1, remaining_length=remaining_length)
        elif current_byte in (SymbolCode.SEPARATOR.value, SymbolCode.TERMINATOR.value) and remaining_length == 0:
            return self.__handle_error_state(previous_byte=current_byte, optional_message=self.__no_interrupt_error_message)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_sep5_state(self, index_to_read: int, remaining_length: int) -> bool:
        '''
        We just read a separator byte (0xFE) after an action block in the reactive AI.

        The next byte must be a reactive condition first byte (0x01-0x12).
        '''
        self.__current_state = StateEnum.SEP5

        remaining_length = max(remaining_length - 1, -1)

        current_byte: int = self.__tokens[index_to_read]

        if ConditionCode.is_valid_condition_code(current_byte) and current_byte is not ConditionCode.UNCONDITIONAL.value:
            return self.__handle_rc1_state(condition_code=ConditionCode(current_byte), index_to_read=index_to_read + 1) 
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_ter2_state(self, previous_byte: int, index_to_read: int, remaining_length: int) -> bool:
        '''
        We finished parsing the reactive AI, and, therefore, the entire AI.
        '''
        self.__current_state = StateEnum.TER2

        remaining_length = max(remaining_length - 1, -1)

        if remaining_length > 0:
            return self.__handle_error_state(previous_byte=previous_byte, optional_message="Not enough bytes were parsed after a NO_INTERRUPT action.")
        elif len(self.__tokens) != index_to_read:
            return self.__handle_error_state(previous_byte=previous_byte, optional_message="Extra bytes were found after parsing the entire AI.")
        else:
            return True
