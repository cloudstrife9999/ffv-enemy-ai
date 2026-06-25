from typing import Optional

from .state_enum import StateEnum
from .stats_and_properties_table import StatsAndPropertiesTable
from .enums.condition_code import ConditionCode
from .enums.target import Target
from .enums.status_table import StatusTable
from .enums.variable import Variable
from .enums.command import Command
from .ability import Ability
from .enums.abilities.dark_arts import DarkArts
from .enums.global_event_table import GlobalEventTable
from .enums.symbol import SymbolCode
from .enums.action_code import ActionCode
from .enums.game_version import GameVersion
from .enemy_ai import EnemyAI


class EnemyAIParser():
    def __init__(self, enemy_id: str, enemy_name: str, enemy_special_ability: str, tokens: bytes, battle_text: dict[int, str], game_version: GameVersion) -> None:
        self.__enemy_id: str = enemy_id
        self.__enemy_name: str = enemy_name
        self.__current_state: StateEnum = StateEnum.START
        self.__tokens: bytes = tokens
        self.__no_interrupt_error_message: str = "Unexpected end of no-interrupt action."
        self.__enemy_ai: EnemyAI = EnemyAI(enemy_id=enemy_id, enemy_name=enemy_name, enemy_special_ability=enemy_special_ability, raw=tokens.hex().upper(), game_version=game_version)
        self.__battle_text: dict[int, str] = battle_text
        self.__game_version: GameVersion = game_version
        self.__current_tokens_group: list[int] = []

    def parse(self) -> bool:
        return self.__handle_start_state(i=0)

    def recompile_tokens(self) -> str:
        return self.__enemy_ai.compile_tokens()

    def get_ai_tokens(self) -> list[list[int]]:
        return self.__enemy_ai.tokens

    def get_parsed_ai(self) -> EnemyAI:
        return self.__enemy_ai

    def __handle_error_state(self, previous_byte: int, optional_message: Optional[str] = None) -> bool:
        if optional_message:
            print(f"[Parser] Ended up in error state for enemy 0x{self.__enemy_id} ({self.__enemy_name}): {optional_message} Previous byte: 0x{previous_byte:02X} in state {self.__current_state.name}.\n - Tokens: {" ".join(f"{b:02X}" for b in self.__tokens)}.")
        else:
            print(f"[Parser] Ended up in error state for enemy 0x{self.__enemy_id} ({self.__enemy_name}): unexpected byte 0x{previous_byte:02X} in state {self.__current_state.name}.\n - Tokens: {" ".join(f"{b:02X}" for b in self.__tokens)}.")

        self.__current_state = StateEnum.ERROR

        return False

    def __handle_start_state(self, i: int) -> bool:
        '''
        We are in the start state, expecting either of the following:
        - The first byte of a non-default condition (0x01-0x0F).
        - The first byte of a default condition (0x00).
        '''
        try:
            self.__current_state = StateEnum.START

            current_byte: int = self.__tokens[i]

            self.__current_tokens_group = [current_byte]

            if not ConditionCode.is_valid_condition_code(current_byte):
                return self.__handle_error_state(previous_byte=current_byte)
            elif ConditionCode(current_byte) is ConditionCode.UNCONDITIONAL:
                return self.__handle_dc1_state(condition_code=ConditionCode(current_byte), i=i + 1)
            else:
                return self.__handle_c1_state(condition_code=ConditionCode(current_byte), i=i + 1)
        except IndexError:
            return self.__handle_error_state(previous_byte=-1, optional_message="Ran out of bytes without finding a terminator byte (0xFF).")

    def __handle_c1_state(self, condition_code: ConditionCode, i: int) -> bool:
        '''
        We just read the first byte of a non-default condition.

        The next byte must be the second byte of a non-default condition.
        '''
        self.__current_state = StateEnum.C1

        current_byte: int = self.__tokens[i]

        self.__current_tokens_group.append(current_byte)

        if condition_code.has_irrelevant_second_byte() or condition_code.has_unrestricted_second_byte():
            return self.__handle_c2_state(condition_code=condition_code, i=i + 1)
        elif condition_code in (ConditionCode.STATUS_EFFECT, ConditionCode.HP_LOWER_THAN_THRESHOLD, ConditionCode.STAT_OR_PROPERTY) and Target.is_valid_target_id(current_byte):
            return self.__handle_c2_state(condition_code=condition_code, i=i + 1)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_c2_state(self, condition_code: ConditionCode, i: int) -> bool:
        '''
        We just read the second byte of a non-default condition.

        The next byte must be the third byte of a non-default condition.
        '''
        self.__current_state = StateEnum.C2

        current_byte: int = self.__tokens[i]

        self.__current_tokens_group.append(current_byte)

        if condition_code.has_irrelevant_third_byte() or condition_code.has_unrestricted_third_byte():
            return self.__handle_c3_state(condition_code=condition_code, i=i + 1)
        elif condition_code is ConditionCode.STATUS_EFFECT and StatusTable.is_valid_status_table_id(current_byte):
            return self.__handle_c3_state(condition_code=condition_code, i=i + 1)
        elif condition_code is ConditionCode.VAR_CHECK and Variable.is_valid_var_id(current_byte):
            return self.__handle_c3_state(condition_code=condition_code, i=i + 1)
        elif condition_code in (ConditionCode.HIT_BY_COMMAND_WITH_ELEMENT, ConditionCode.HIT_BY_COMMAND_WITH_CATEGORY) and Command.is_valid_command_id(current_byte):
            return self.__handle_c3_state(condition_code=condition_code, i=i + 1)
        elif condition_code is ConditionCode.HIT_BY_SPELL and Ability.is_valid_id(current_byte):
            return self.__handle_c3_state(condition_code=condition_code, i=i + 1)
        elif condition_code is ConditionCode.STAT_OR_PROPERTY and StatsAndPropertiesTable.is_valid_party_member_property_offset(self.__game_version, current_byte):
            return self.__handle_c3_state(condition_code=condition_code, i=i + 1)
        elif condition_code is ConditionCode.GLOBAL_EVENT_FLAGS and GlobalEventTable.is_valid_global_event_table_id(current_byte):
            return self.__handle_c3_state(condition_code=condition_code, i=i + 1)
        else:
            return self.__handle_error_state(previous_byte=current_byte)
            
    def __handle_c3_state(self, condition_code: ConditionCode, i: int) -> bool:
        '''
        We just read the third byte of a non-default condition.

        The next byte must be the fourth byte of a non-default condition.
        '''
        self.__current_state = StateEnum.C3

        current_byte: int = self.__tokens[i]

        self.__current_tokens_group.append(current_byte)

        if condition_code.has_irrelevant_fourth_byte() or condition_code.has_unrestricted_fourth_byte():
            return self.__handle_c4_state(i=i + 1)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_c4_state(self, i: int) -> bool:
        '''
        We just read the fourth byte of a non-default condition.

        The next byte must be either of the following:
        * A separator byte (0xFE) if no more conditions are to be read for this rule.
        * The first byte of a non-default condition (0x01-0x0F) if more conditions are to be read for this rule.
        '''
        self.__current_state = StateEnum.C4

        self.__enemy_ai.add_condition(tokens=self.__current_tokens_group)

        current_byte: int = self.__tokens[i]

        self.__current_tokens_group = [current_byte]

        if current_byte is SymbolCode.SEPARATOR.value:
            return self.__handle_sep1_state(i=i + 1)
        elif ConditionCode.is_valid_condition_code(current_byte):
            return self.__handle_c1_state(condition_code=ConditionCode(current_byte), i=i + 1)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_sep1_state(self, i: int) -> bool:
        '''
        We just read a separator byte (0xFE) after the fourth byte of a non-default condition.

        The next byte must be a simple action byte (0x00-0xEF) or a complex action first byte (0xF2-0xFD).
        '''
        self.__current_state = StateEnum.SEP1

        self.__enemy_ai.add_separator(tokens=self.__current_tokens_group)

        current_byte: int = self.__tokens[i]

        self.__current_tokens_group = [current_byte]

        # Because of some ID collisions, the order of the checks is critical here (i.e., Dark Arts abilities share the same IDs with some AI commands).
        # First, non-dark arts abilities must be checked, then complex action codes, and finally dark arts abilities.
        if Ability.is_valid_non_dark_arts_id(current_byte):
            return self.__handle_sa_state(i=i + 1, f7_counter=-1)
        elif ActionCode.is_valid_four_byte_action_code(current_byte):
            return self.__handle_ca1_state(action_code=ActionCode(current_byte), i=i + 1, f7_counter=-1)
        elif DarkArts.is_valid_id(current_byte):
            return self.__handle_sa_state(i=i + 1, f7_counter=-1)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_sa_state(self, i: int, f7_counter: int) -> bool:
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

        self.__enemy_ai.add_action(tokens=self.__current_tokens_group, battle_text=self.__battle_text)

        if f7_counter == 0:
            # We found the last sub-action of a no-interrupt action whose length does not cover a separator or terminator byte.
            self.__enemy_ai.finalise_no_interrupt_action(additional_length=False)

        f7_counter = max(f7_counter - 1, -1)

        current_byte: int = self.__tokens[i]

        self.__current_tokens_group = [current_byte]

        if current_byte is SymbolCode.SEPARATOR.value:
            return self.__handle_sep2_state(i=i + 1, f7_counter=f7_counter)
        # Because of some ID collisions, the order of the checks is critical here (i.e., Dark Arts abilities share the same IDs with some AI commands).
        # First, non-dark arts abilities must be checked, then complex action codes, and finally dark arts abilities.
        elif Ability.is_valid_non_dark_arts_id(current_byte):
            return self.__handle_sa_state(i=i + 1, f7_counter=f7_counter)
        elif ActionCode.is_valid_four_byte_action_code(current_byte):
            return self.__handle_ca1_state(action_code=ActionCode(current_byte), i=i + 1, f7_counter=f7_counter)
        elif DarkArts.is_valid_id(current_byte):
            return self.__handle_sa_state(i=i + 1, f7_counter=f7_counter)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_ca1_state(self, action_code: ActionCode, i: int, f7_counter: int) -> bool:
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

        f7_counter = max(f7_counter - 1, -1)

        current_byte: int = self.__tokens[i]

        self.__current_tokens_group.append(current_byte)

        # A no-interrupt action cannot end here.
        if f7_counter == 0:
            return self.__handle_error_state(previous_byte=current_byte, optional_message=self.__no_interrupt_error_message)
        elif action_code is ActionCode.GBA_RANDOM_SELECTION and Ability.is_valid_id(current_byte):
            return self.__handle_ca2_state(action_code=action_code, sub_action_code=None, i=i + 1, f7_counter=f7_counter)
        elif action_code is ActionCode.RANDOM_SELECTION and Ability.is_valid_non_dark_arts_id(current_byte):
            return self.__handle_ca2_state(action_code=action_code, sub_action_code=None, i=i + 1, f7_counter=f7_counter)
        elif action_code is ActionCode.AI_COMMAND and ActionCode.NO_INTERRUPT.value == current_byte:
            return self.__handle_ca2_state(action_code=action_code, sub_action_code=ActionCode.NO_INTERRUPT, i=i + 1, f7_counter=f7_counter)
        elif action_code is ActionCode.AI_COMMAND and ActionCode.is_valid_three_byte_action_code(current_byte):
            return self.__handle_ca2_state(action_code=action_code, sub_action_code=ActionCode(current_byte), i=i + 1, f7_counter=f7_counter)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_ca2_state(self, action_code: ActionCode, sub_action_code: Optional[ActionCode], i: int, f7_counter: int) -> bool:
        '''
        We just read either of the following:
        - A simple action byte (as part of a 4-byte random selection action).
        - A valid 1-byte action code of a 3-byte action (as part of a 4-byte AI command).

        The next byte must be one of the following:
        - A simple action byte (0x00-0xEF) if and only if the previous byte was a simple action byte (as part of a 4-byte random selection action).
        - The second byte of a 3-byte action otherwise (as part of a 4-byte AI command).
        '''
        self.__current_state = StateEnum.CA2

        f7_counter = max(f7_counter - 1, -1)

        current_byte: int = self.__tokens[i]

        self.__current_tokens_group.append(current_byte)

        # A no-interrupt action cannot end here.
        if f7_counter == 0:
            return self.__handle_error_state(previous_byte=current_byte, optional_message=self.__no_interrupt_error_message)
        elif sub_action_code is ActionCode.NO_INTERRUPT and current_byte >= 2:  # The minimum length is the size of 2 simple actions (1 byte each).
            # +1 because the next byte is not covered by the declared length of a no-interrupt action.
            return self.__handle_ca3_state(action_code=action_code, i=i + 1, f7_counter=current_byte + 1)
        elif action_code is ActionCode.GBA_RANDOM_SELECTION and Ability.is_valid_id(current_byte):
            return self.__handle_ca3_state(action_code=action_code, i=i + 1, f7_counter=f7_counter)
        elif action_code is ActionCode.RANDOM_SELECTION and Ability.is_valid_non_dark_arts_id(current_byte):
            return self.__handle_ca3_state(action_code=action_code, i=i + 1, f7_counter=f7_counter)
        elif action_code is not ActionCode.AI_COMMAND:
            return self.__handle_error_state(previous_byte=current_byte)
        else:
            return self.__handle_ca2_state_helper(action_code=action_code, sub_action_code=sub_action_code, current_byte=current_byte, i=i, f7_counter=f7_counter)

    def __handle_ca2_state_helper(self, action_code: ActionCode, sub_action_code: Optional[ActionCode], current_byte: int, i: int, f7_counter: int) -> bool:
        if sub_action_code in (ActionCode.SET_ENEMY_TO_SHOW, ActionCode.UNKNOWN_F5_ACTION, ActionCode.DISPLAY_MESSAGE, ActionCode.FULL_SCREEN_EFFECT):
            return self.__handle_ca3_state(action_code=action_code, i=i + 1, f7_counter=f7_counter)
        elif sub_action_code is ActionCode.SET_TARGET and Target.is_valid_target_id(current_byte):
            return self.__handle_ca3_state(action_code=action_code, i=i + 1, f7_counter=f7_counter)
        elif sub_action_code is ActionCode.SET_VARIABLE and Variable.is_valid_var_id(current_byte):
            return self.__handle_ca3_state(action_code=action_code, i=i + 1, f7_counter=f7_counter)
        elif sub_action_code is ActionCode.SET_GLOBAL_EVENT_FLAG and GlobalEventTable.is_valid_global_event_table_id(current_byte):
            return self.__handle_ca3_state(action_code=action_code, i=i + 1, f7_counter=f7_counter)
        elif sub_action_code is ActionCode.SET_STATS_OR_TOGGLE_STATUS and StatsAndPropertiesTable.is_valid_party_member_property_offset(self.__game_version, current_byte):
            return self.__handle_ca3_state(action_code=action_code, i=i + 1, f7_counter=f7_counter)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_ca3_state(self, action_code: ActionCode, i: int, f7_counter: int) -> bool:
        '''
        We just read either of the following:
        - A simple action byte (as part of a 4-byte random selection action).
        - The second byte of a 3-byte action (as part of a 4-byte AI command).

        The next byte must be one of the following:
        - A simple action byte (0x00-0xEF) if and only if the previous byte was a simple action byte (as part of a 4-byte random selection action).
        - The third byte of a 3-byte action otherwise (as part of a 4-byte AI command).
        '''
        self.__current_state = StateEnum.CA3

        f7_counter = max(f7_counter - 1, -1)

        current_byte: int = self.__tokens[i]

        self.__current_tokens_group.append(current_byte)

        if action_code is ActionCode.GBA_RANDOM_SELECTION and Ability.is_valid_id(current_byte):
            return self.__handle_ca4_state(i=i + 1, f7_counter=f7_counter)
        elif action_code is ActionCode.RANDOM_SELECTION and Ability.is_valid_non_dark_arts_id(current_byte):
            return self.__handle_ca4_state(i=i + 1, f7_counter=f7_counter)
        elif action_code is ActionCode.AI_COMMAND:  # The last byte is unrestricted for 3-byte actions (as part of a 4-byte command).
            return self.__handle_ca4_state(i=i + 1, f7_counter=f7_counter)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_ca4_state(self, i: int, f7_counter: int) -> bool:
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

        self.__enemy_ai.add_action(tokens=self.__current_tokens_group, battle_text=self.__battle_text)

        if f7_counter == 0:
            # We found the last sub-action of a no-interrupt action whose length does not cover a separator or terminator byte.
            self.__enemy_ai.finalise_no_interrupt_action(additional_length=False)

        f7_counter = max(f7_counter - 1, -1)

        current_byte: int = self.__tokens[i]

        self.__current_tokens_group = [current_byte]

        # Because of some ID collisions, the order of the checks is critical here (i.e., Dark Arts abilities share the same IDs with some AI commands).
        # First, non-dark arts abilities must be checked, then complex action codes, and finally dark arts abilities.
        if Ability.is_valid_non_dark_arts_id(current_byte):
            return self.__handle_sa_state(i=i + 1, f7_counter=f7_counter)
        elif ActionCode.is_valid_four_byte_action_code(current_byte):
            return self.__handle_ca1_state(action_code=ActionCode(current_byte), i=i + 1, f7_counter=f7_counter)
        elif DarkArts.is_valid_id(current_byte):
            return self.__handle_sa_state(i=i + 1, f7_counter=f7_counter)
        elif current_byte is SymbolCode.SEPARATOR.value:
            return self.__handle_sep2_state(i=i + 1, f7_counter=f7_counter)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_sep2_state(self, i: int, f7_counter: int) -> bool:
        '''
        We just read a separator byte (0xFE) after a non-default action block in the active AI.

        The next byte must be either of the following:
        - The first byte of a default condition (0x00), if there are no more non-default rules in the active AI.
        - The first byte of a non-default condition (0x01-0x0F) otherwise.
        '''
        self.__current_state = StateEnum.SEP2

        if self.__enemy_ai.has_lingering_no_interrupt_action():
            # The separator that brought us here is covered by the length of a lingering no-interrupt action.
            self.__enemy_ai.finalise_no_interrupt_action(additional_length=True)

        self.__enemy_ai.add_separator(tokens=self.__current_tokens_group)

        f7_counter = max(f7_counter - 1, -1)

        current_byte: int = self.__tokens[i]

        self.__current_tokens_group = [current_byte]

        if current_byte is ConditionCode.UNCONDITIONAL.value:
            return self.__handle_dc1_state(condition_code=ConditionCode.UNCONDITIONAL, i=i + 1)
        elif ConditionCode.is_valid_condition_code(current_byte):
            return self.__handle_c1_state(condition_code=ConditionCode(current_byte), i=i + 1) 
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_dc1_state(self, condition_code: ConditionCode, i: int) -> bool:
        '''
        We just read the first byte of a default condition.

        The next byte must be the second byte of a default condition.
        '''
        self.__current_state = StateEnum.DC1

        current_byte: int = self.__tokens[i]

        self.__current_tokens_group.append(current_byte)

        if condition_code.has_irrelevant_second_byte() or condition_code.has_unrestricted_second_byte():
            return self.__handle_dc2_state(condition_code=condition_code, i=i + 1)
        elif condition_code in (ConditionCode.STATUS_EFFECT, ConditionCode.HP_LOWER_THAN_THRESHOLD, ConditionCode.STAT_OR_PROPERTY) and Target.is_valid_target_id(current_byte):
            return self.__handle_dc2_state(condition_code=condition_code, i=i + 1)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_dc2_state(self, condition_code: ConditionCode, i: int) -> bool:
        '''
        We just read the second byte of a default condition.

        The next byte must be the third byte of a default condition.
        '''
        self.__current_state = StateEnum.DC2

        current_byte: int = self.__tokens[i]

        self.__current_tokens_group.append(current_byte)

        if condition_code.has_irrelevant_third_byte() or condition_code.has_unrestricted_third_byte():
            return self.__handle_dc3_state(condition_code=condition_code, i=i + 1)
        elif condition_code is ConditionCode.STATUS_EFFECT and StatusTable.is_valid_status_table_id(current_byte):
            return self.__handle_dc3_state(condition_code=condition_code, i=i + 1)
        elif condition_code is ConditionCode.VAR_CHECK and Variable.is_valid_var_id(current_byte):
            return self.__handle_dc3_state(condition_code=condition_code, i=i + 1)
        elif condition_code in (ConditionCode.HIT_BY_COMMAND_WITH_ELEMENT, ConditionCode.HIT_BY_COMMAND_WITH_CATEGORY) and Command.is_valid_command_id(current_byte):
            return self.__handle_dc3_state(condition_code=condition_code, i=i + 1)
        elif condition_code is ConditionCode.HIT_BY_SPELL and Ability.is_valid_id(current_byte):
            return self.__handle_dc3_state(condition_code=condition_code, i=i + 1)
        elif condition_code is ConditionCode.STAT_OR_PROPERTY and StatsAndPropertiesTable.is_valid_party_member_property_offset(self.__game_version, current_byte):
            return self.__handle_dc3_state(condition_code=condition_code, i=i + 1)
        elif condition_code is ConditionCode.GLOBAL_EVENT_FLAGS and GlobalEventTable.is_valid_global_event_table_id(current_byte):
            return self.__handle_dc3_state(condition_code=condition_code, i=i + 1)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_dc3_state(self, condition_code: ConditionCode, i: int) -> bool:
        '''
        We just read the third byte of a default condition.

        The next byte must be the fourth byte of a default condition.
        '''
        self.__current_state = StateEnum.DC3

        current_byte: int = self.__tokens[i]

        self.__current_tokens_group.append(current_byte)

        if condition_code.has_irrelevant_fourth_byte() or condition_code.has_unrestricted_fourth_byte():
            return self.__handle_dc4_state(i=i + 1)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_dc4_state(self, i: int) -> bool:
        '''
        We just read the fourth byte of a default condition.

        The next byte must be a separator byte (0xFE), as the default condition cannot be in AND with any other conditions (default or non-default).
        '''
        self.__current_state = StateEnum.DC4

        self.__enemy_ai.add_condition(tokens=self.__current_tokens_group)

        current_byte: int = self.__tokens[i]

        self.__current_tokens_group = [current_byte]

        if current_byte is SymbolCode.SEPARATOR.value:
            return self.__handle_sep3_state(i=i + 1)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_sep3_state(self, i: int) -> bool:
        '''
        We just read a separator byte (0xFE) after the fourth byte of a default condition.

        The next byte must be a simple action byte (0x00-0xEF) or a complex action first byte (0xF2-0xFD).
        '''
        self.__current_state = StateEnum.SEP3

        self.__enemy_ai.add_separator(tokens=self.__current_tokens_group)

        current_byte: int = self.__tokens[i]

        self.__current_tokens_group = [current_byte]

        # Because of some ID collisions, the order of the checks is critical here (i.e., Dark Arts abilities share the same IDs with some AI commands).
        # First, non-dark arts abilities must be checked, then complex action codes, and finally dark arts abilities.
        if Ability.is_valid_non_dark_arts_id(current_byte):
            return self.__handle_sda_state(i=i + 1, f7_counter=-1)
        elif ActionCode.is_valid_four_byte_action_code(current_byte):
            return self.__handle_cda1_state(action_code=ActionCode(current_byte), i=i + 1, f7_counter=-1)
        elif DarkArts.is_valid_id(current_byte):
            return self.__handle_sda_state(i=i + 1, f7_counter=-1)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_sda_state(self, i: int, f7_counter: int) -> bool:
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

        self.__enemy_ai.add_action(tokens=self.__current_tokens_group, battle_text=self.__battle_text)

        if f7_counter == 0:
            # We found the last sub-action of a no-interrupt action whose length does not cover a separator or terminator byte.
            self.__enemy_ai.finalise_no_interrupt_action(additional_length=False)

        f7_counter = max(f7_counter - 1, -1)

        current_byte: int = self.__tokens[i]

        self.__current_tokens_group = [current_byte]

        if current_byte is SymbolCode.TERMINATOR.value:
            return self.__handle_ter1_state(i=i + 1, f7_counter=f7_counter)
        # Because of some ID collisions, the order of the checks is critical here (i.e., Dark Arts abilities share the same IDs with some AI commands).
        # First, non-dark arts abilities must be checked, then complex action codes, and finally dark arts abilities.
        elif Ability.is_valid_non_dark_arts_id(current_byte):
            return self.__handle_sda_state(i=i + 1, f7_counter=f7_counter)
        elif ActionCode.is_valid_four_byte_action_code(current_byte):
            return self.__handle_cda1_state(action_code=ActionCode(current_byte), i=i + 1, f7_counter=f7_counter)
        elif DarkArts.is_valid_id(current_byte):
            return self.__handle_sda_state(i=i + 1, f7_counter=f7_counter)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_cda1_state(self, action_code: ActionCode, i: int, f7_counter: int) -> bool:
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

        f7_counter = max(f7_counter - 1, -1)

        current_byte: int = self.__tokens[i]

        self.__current_tokens_group.append(current_byte)

        # A no-interrupt action cannot end here.
        if f7_counter == 0:
            return self.__handle_error_state(previous_byte=current_byte, optional_message=self.__no_interrupt_error_message)
        elif action_code is ActionCode.GBA_RANDOM_SELECTION and Ability.is_valid_id(current_byte):
            return self.__handle_cda2_state(action_code=action_code, sub_action_code=None, i=i + 1, f7_counter=f7_counter)
        elif action_code is ActionCode.RANDOM_SELECTION and Ability.is_valid_non_dark_arts_id(current_byte):
            return self.__handle_cda2_state(action_code=action_code, sub_action_code=None, i=i + 1, f7_counter=f7_counter)
        elif action_code is ActionCode.AI_COMMAND and ActionCode.is_valid_three_byte_action_code(current_byte):
            return self.__handle_cda2_state(action_code=action_code, sub_action_code=ActionCode(current_byte), i=i + 1, f7_counter=f7_counter)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_cda2_state(self, action_code: ActionCode, sub_action_code: Optional[ActionCode], i: int, f7_counter: int) -> bool:
        '''
        We just read either of the following:
        - A simple action byte (as part of a 4-byte random selection action).
        - A valid 1-byte action code of a 3-byte action (as part of a 4-byte AI command action).

        The next byte must be one of the following:
        - A simple action byte (0x00-0xEF) if and only if the previous byte was a simple action byte (as part of a 4-byte random selection action).
        - The second byte of a 3-byte action otherwise (as part of a 4-byte AI command action).
        '''
        self.__current_state = StateEnum.CDA2

        f7_counter = max(f7_counter - 1, -1)

        current_byte: int = self.__tokens[i]

        self.__current_tokens_group.append(current_byte)

        # A no-interrupt action cannot end here.
        if f7_counter == 0:
            return self.__handle_error_state(previous_byte=current_byte, optional_message=self.__no_interrupt_error_message)
        elif sub_action_code is ActionCode.NO_INTERRUPT and current_byte >= 2:  # The minimum length is the size of 2 simple actions (1 byte each).
            # +1 because the next byte is not covered by the declared length of a no-interrupt action.
            return self.__handle_cda3_state(action_code=action_code, i=i + 1, f7_counter=current_byte + 1)
        elif action_code is ActionCode.GBA_RANDOM_SELECTION and Ability.is_valid_id(current_byte):
            return self.__handle_cda3_state(action_code=action_code, i=i + 1, f7_counter=f7_counter)
        elif action_code is ActionCode.RANDOM_SELECTION and Ability.is_valid_non_dark_arts_id(current_byte):
            return self.__handle_cda3_state(action_code=action_code, i=i + 1, f7_counter=f7_counter)
        elif action_code is not ActionCode.AI_COMMAND:
            return self.__handle_error_state(previous_byte=current_byte)
        else:
            return self.__handle_cda2_state_helper(action_code=action_code, sub_action_code=sub_action_code, current_byte=current_byte, i=i, f7_counter=f7_counter)

    def __handle_cda2_state_helper(self, action_code: ActionCode, sub_action_code: Optional[ActionCode], current_byte: int, i: int, f7_counter: int) -> bool:
        if sub_action_code in (ActionCode.SET_ENEMY_TO_SHOW, ActionCode.UNKNOWN_F5_ACTION, ActionCode.DISPLAY_MESSAGE, ActionCode.FULL_SCREEN_EFFECT):
            return self.__handle_cda3_state(action_code=action_code, i=i + 1, f7_counter=f7_counter)
        elif sub_action_code is ActionCode.SET_TARGET and Target.is_valid_target_id(current_byte):
            return self.__handle_cda3_state(action_code=action_code, i=i + 1, f7_counter=f7_counter)
        elif sub_action_code is ActionCode.SET_VARIABLE and Variable.is_valid_var_id(current_byte):
            return self.__handle_cda3_state(action_code=action_code, i=i + 1, f7_counter=f7_counter)
        elif sub_action_code is ActionCode.SET_GLOBAL_EVENT_FLAG and GlobalEventTable.is_valid_global_event_table_id(current_byte):
            return self.__handle_cda3_state(action_code=action_code, i=i + 1, f7_counter=f7_counter)
        elif sub_action_code is ActionCode.SET_STATS_OR_TOGGLE_STATUS and StatsAndPropertiesTable.is_valid_party_member_property_offset(self.__game_version, current_byte):
            return self.__handle_cda3_state(action_code=action_code, i=i + 1, f7_counter=f7_counter)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_cda3_state(self, action_code: ActionCode, i: int, f7_counter: int) -> bool:
        '''
        We just read either of the following:
        - A simple action byte (as part of a 4-byte random selection action).
        - The second byte of a 3-byte action (as part of a 4-byte AI command action).

        The next byte must be one of the following:
        - A simple action byte (0x00-0xEF) if and only if the previous byte was a simple action byte (as part of a 4-byte random selection action).
        - The third byte of a 3-byte action otherwise (as part of a 4-byte AI command action).
        '''
        self.__current_state = StateEnum.CDA3

        f7_counter = max(f7_counter - 1, -1)

        current_byte: int = self.__tokens[i]

        self.__current_tokens_group.append(current_byte)

        if action_code is ActionCode.GBA_RANDOM_SELECTION and Ability.is_valid_id(current_byte):
            return self.__handle_cda4_state(i=i + 1, f7_counter=f7_counter)
        elif action_code is ActionCode.RANDOM_SELECTION and Ability.is_valid_non_dark_arts_id(current_byte):
            return self.__handle_cda4_state(i=i + 1, f7_counter=f7_counter)
        elif action_code is ActionCode.AI_COMMAND:  # The last byte is unrestricted for 3-byte actions (as part of a 4-byte command).
            return self.__handle_cda4_state(i=i + 1, f7_counter=f7_counter)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_cda4_state(self, i: int, f7_counter: int) -> bool:
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

        self.__enemy_ai.add_action(tokens=self.__current_tokens_group, battle_text=self.__battle_text)

        if f7_counter == 0:
            # We found the last sub-action of a no-interrupt action whose length does not cover a separator or terminator byte.
            self.__enemy_ai.finalise_no_interrupt_action(additional_length=False)

        f7_counter = max(f7_counter - 1, -1)

        current_byte: int = self.__tokens[i]

        self.__current_tokens_group = [current_byte]

        # Because of some ID collisions, the order of the checks is critical here (i.e., Dark Arts abilities share the same IDs with some AI commands).
        # First, non-dark arts abilities must be checked, then complex action codes, and finally dark arts abilities.
        if Ability.is_valid_non_dark_arts_id(current_byte):
            return self.__handle_sda_state(i=i + 1, f7_counter=f7_counter)
        elif ActionCode.is_valid_four_byte_action_code(current_byte):
            return self.__handle_cda1_state(action_code=ActionCode(current_byte), i=i + 1, f7_counter=f7_counter)
        elif DarkArts.is_valid_id(current_byte):
            return self.__handle_sda_state(i=i + 1, f7_counter=f7_counter)
        elif current_byte is SymbolCode.TERMINATOR.value:
            return self.__handle_ter1_state(i=i + 1, f7_counter=f7_counter)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_ter1_state(self, i: int, f7_counter: int) -> bool:
        '''
        We just read a terminator byte (0xFF) after the last action in the default action block (and in the active AI as well).

        The next byte must be either of the following:
        - Another terminator byte (0xFF), if the reactive AI is empty.
        - The first byte of a reactive condition (0x01-0x0F) otherwise.
        '''
        self.__current_state = StateEnum.TER1

        if self.__enemy_ai.has_lingering_no_interrupt_action():
            # The terminator that brought us here is covered by the length of a lingering no-interrupt action.
            self.__enemy_ai.finalise_no_interrupt_action(additional_length=True)

        self.__enemy_ai.add_terminator(tokens=self.__current_tokens_group)

        f7_counter = max(f7_counter - 1, -1)

        current_byte: int = self.__tokens[i]

        self.__current_tokens_group = [current_byte]

        if current_byte is SymbolCode.TERMINATOR.value:
            return self.__handle_ter2_state(previous_byte=current_byte, i=i + 1, f7_counter=f7_counter)
        elif ConditionCode.is_valid_condition_code(current_byte) and current_byte is not ConditionCode.UNCONDITIONAL.value:
            return self.__handle_rc1_state(condition_code=ConditionCode(current_byte), i=i + 1)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_rc1_state(self, condition_code: ConditionCode, i: int) -> bool:
        '''
        We just read the first byte of a reactive condition in the reactive AI.

        The next byte must be the second byte of a reactive condition.
        '''
        self.__current_state = StateEnum.RC1

        current_byte: int = self.__tokens[i]

        self.__current_tokens_group.append(current_byte)

        if condition_code.has_irrelevant_second_byte() or condition_code.has_unrestricted_second_byte():
            return self.__handle_rc2_state(condition_code=condition_code, i=i + 1)
        elif condition_code in (ConditionCode.STATUS_EFFECT, ConditionCode.HP_LOWER_THAN_THRESHOLD, ConditionCode.STAT_OR_PROPERTY) and Target.is_valid_target_id(current_byte):
            return self.__handle_rc2_state(condition_code=condition_code, i=i + 1)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_rc2_state(self, condition_code: ConditionCode, i: int) -> bool:
        '''
        We just read the second byte of a reactive condition in the reactive AI.

        The next byte must be the third byte of a reactive condition.
        '''
        self.__current_state = StateEnum.RC2

        current_byte: int = self.__tokens[i]

        self.__current_tokens_group.append(current_byte)

        if condition_code.has_irrelevant_third_byte() or condition_code.has_unrestricted_third_byte():
            return self.__handle_rc3_state(condition_code=condition_code, i=i + 1)
        elif condition_code is ConditionCode.STATUS_EFFECT and StatusTable.is_valid_status_table_id(current_byte):
            return self.__handle_rc3_state(condition_code=condition_code, i=i + 1)
        elif condition_code is ConditionCode.VAR_CHECK and Variable.is_valid_var_id(current_byte):
            return self.__handle_rc3_state(condition_code=condition_code, i=i + 1)
        elif condition_code in (ConditionCode.HIT_BY_COMMAND_WITH_ELEMENT, ConditionCode.HIT_BY_COMMAND_WITH_CATEGORY) and Command.is_valid_command_id(current_byte):
            return self.__handle_rc3_state(condition_code=condition_code, i=i + 1)
        elif condition_code is ConditionCode.HIT_BY_SPELL and Ability.is_valid_id(current_byte):
            return self.__handle_rc3_state(condition_code=condition_code, i=i + 1)
        elif condition_code is ConditionCode.STAT_OR_PROPERTY and StatsAndPropertiesTable.is_valid_party_member_property_offset(self.__game_version, current_byte):
            return self.__handle_rc3_state(condition_code=condition_code, i=i + 1)
        elif condition_code is ConditionCode.GLOBAL_EVENT_FLAGS and GlobalEventTable.is_valid_global_event_table_id(current_byte):
            return self.__handle_rc3_state(condition_code=condition_code, i=i + 1)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_rc3_state(self, condition_code: ConditionCode, i: int) -> bool:
        '''
        We just read the third byte of a reactive condition in the reactive AI.

        The next byte must be the fourth byte of a reactive condition.
        '''
        self.__current_state = StateEnum.RC3

        current_byte: int = self.__tokens[i]

        self.__current_tokens_group.append(current_byte)

        if condition_code.has_irrelevant_fourth_byte() or condition_code.has_unrestricted_fourth_byte():
            return self.__handle_rc4_state(i=i + 1)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_rc4_state(self, i: int) -> bool:
        '''
        We just read the fourth byte of a reactive condition in the reactive AI.

        The next byte must be either of the following:
        * A separator byte (0xFE) if no more conditions are to be read for this rule.
        * The first byte of a reactive condition (0x01-0x0F) if more conditions are to be read for this rule.
        '''
        self.__current_state = StateEnum.RC4

        self.__enemy_ai.add_condition(tokens=self.__current_tokens_group)

        current_byte: int = self.__tokens[i]

        self.__current_tokens_group = [current_byte]

        if current_byte is SymbolCode.SEPARATOR.value:
            return self.__handle_sep4_state(i=i + 1)
        elif ConditionCode.is_valid_condition_code(current_byte):
            return self.__handle_rc1_state(condition_code=ConditionCode(current_byte), i=i + 1)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_sep4_state(self, i: int) -> bool:
        '''
        We just read a separator byte (0xFE) after the fourth byte of a reactive condition.

        The next byte must be a simple action byte (0x00-0xEF) or a complex action first byte (0xF2-0xFD).
        '''
        self.__current_state = StateEnum.SEP4

        self.__enemy_ai.add_separator(tokens=self.__current_tokens_group)

        current_byte: int = self.__tokens[i]

        self.__current_tokens_group = [current_byte]

        # Because of some ID collisions, the order of the checks is critical here (i.e., Dark Arts abilities share the same IDs with some AI commands).
        # First, non-dark arts abilities must be checked, then complex action codes, and finally dark arts abilities.
        if Ability.is_valid_non_dark_arts_id(current_byte):
            return self.__handle_rsa_state(i=i + 1, f7_counter=-1)
        elif ActionCode.is_valid_four_byte_action_code(current_byte):
            return self.__handle_rca1_state(action_code=ActionCode(current_byte), i=i + 1, f7_counter=-1)
        elif DarkArts.is_valid_id(current_byte):
            return self.__handle_rsa_state(i=i + 1, f7_counter=-1)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_rsa_state(self, i: int, f7_counter: int) -> bool:
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

        self.__enemy_ai.add_action(tokens=self.__current_tokens_group, battle_text=self.__battle_text)

        if f7_counter == 0:
            # We found the last sub-action of a no-interrupt action whose length does not cover a separator or terminator byte.
            self.__enemy_ai.finalise_no_interrupt_action(additional_length=False)

        f7_counter = max(f7_counter - 1, -1)

        current_byte: int = self.__tokens[i]

        self.__current_tokens_group = [current_byte]

        if current_byte is SymbolCode.SEPARATOR.value:
            return self.__handle_sep5_state(i=i + 1, f7_counter=f7_counter)
        elif current_byte is SymbolCode.TERMINATOR.value:
            return self.__handle_ter2_state(previous_byte=current_byte, i=i + 1, f7_counter=f7_counter)
        # Because of some ID collisions, the order of the checks is critical here (i.e., Dark Arts abilities share the same IDs with some AI commands).
        # First, non-dark arts abilities must be checked, then complex action codes, and finally dark arts abilities.
        elif Ability.is_valid_non_dark_arts_id(current_byte):
            return self.__handle_rsa_state(i=i + 1, f7_counter=f7_counter)
        elif ActionCode.is_valid_four_byte_action_code(current_byte):
            return self.__handle_rca1_state(action_code=ActionCode(current_byte), i=i + 1, f7_counter=f7_counter)
        elif DarkArts.is_valid_id(current_byte):
            return self.__handle_rsa_state(i=i + 1, f7_counter=f7_counter)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_rca1_state(self, action_code: ActionCode, i: int, f7_counter: int) -> bool:
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

        f7_counter = max(f7_counter - 1, -1)

        current_byte: int = self.__tokens[i]

        self.__current_tokens_group.append(current_byte)

        # A no-interrupt action cannot end here.
        if f7_counter == 0:
            return self.__handle_error_state(previous_byte=current_byte, optional_message=self.__no_interrupt_error_message)
        elif action_code is ActionCode.GBA_RANDOM_SELECTION and Ability.is_valid_id(current_byte):
            return self.__handle_rca2_state(action_code=action_code, sub_action_code=None, i=i + 1, f7_counter=f7_counter)
        elif action_code is ActionCode.RANDOM_SELECTION and Ability.is_valid_non_dark_arts_id(current_byte):
            return self.__handle_rca2_state(action_code=action_code, sub_action_code=None, i=i + 1, f7_counter=f7_counter)
        elif action_code is ActionCode.AI_COMMAND and ActionCode.is_valid_three_byte_action_code(current_byte):
            return self.__handle_rca2_state(action_code=action_code, sub_action_code=ActionCode(current_byte), i=i + 1, f7_counter=f7_counter)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_rca2_state(self, action_code: ActionCode, sub_action_code: Optional[ActionCode], i: int, f7_counter: int) -> bool:
        '''
        We just read either of the following:
        - A simple action byte (as part of a 4-byte random selection action).
        - A valid 1-byte action code of a 3-byte action (as part of a 4-byte AI command).

        The next byte must be one of the following:
        - A simple action byte (0x00-0xEF) if and only if the previous byte was a simple action byte (as part of a 4-byte random selection action).
        - The second byte of a 3-byte action otherwise (as part of a 4-byte AI command).
        '''
        self.__current_state = StateEnum.RCA2

        f7_counter = max(f7_counter - 1, -1)

        current_byte: int = self.__tokens[i]

        self.__current_tokens_group.append(current_byte)

        # A no-interrupt action cannot end here.
        if f7_counter == 0:
            return self.__handle_error_state(previous_byte=current_byte, optional_message=self.__no_interrupt_error_message)
        elif sub_action_code is ActionCode.NO_INTERRUPT and current_byte >= 2:  # The minimum length is the size of 2 simple actions (1 byte each).
            # +1 because the next byte is not covered by the declared length of a no-interrupt action.
            return self.__handle_rca3_state(action_code=action_code, i=i + 1, f7_counter=current_byte + 1)
        elif action_code is ActionCode.GBA_RANDOM_SELECTION and (Ability.is_valid_id(current_byte) or DarkArts.is_valid_id(current_byte)):
            return self.__handle_rca3_state(action_code=action_code, i=i + 1, f7_counter=f7_counter)
        elif action_code is ActionCode.RANDOM_SELECTION and Ability.is_valid_id(current_byte):
            return self.__handle_rca3_state(action_code=action_code, i=i + 1, f7_counter=f7_counter)
        elif action_code is not ActionCode.AI_COMMAND:
            return self.__handle_error_state(previous_byte=current_byte)
        else:
            return self.__handle_rca2_state_helper(action_code=action_code, sub_action_code=sub_action_code, current_byte=current_byte, i=i, f7_counter=f7_counter)

    def __handle_rca2_state_helper(self, action_code: ActionCode, sub_action_code: Optional[ActionCode], current_byte: int, i: int, f7_counter: int) -> bool:
        if sub_action_code in (ActionCode.SET_ENEMY_TO_SHOW, ActionCode.UNKNOWN_F5_ACTION, ActionCode.DISPLAY_MESSAGE, ActionCode.FULL_SCREEN_EFFECT):
            return self.__handle_rca3_state(action_code=action_code, i=i + 1, f7_counter=f7_counter)
        elif sub_action_code is ActionCode.SET_TARGET and Target.is_valid_target_id(current_byte):
            return self.__handle_rca3_state(action_code=action_code, i=i + 1, f7_counter=f7_counter)
        elif sub_action_code is ActionCode.SET_VARIABLE and Variable.is_valid_var_id(current_byte):
            return self.__handle_rca3_state(action_code=action_code, i=i + 1, f7_counter=f7_counter)
        elif sub_action_code is ActionCode.SET_GLOBAL_EVENT_FLAG and GlobalEventTable.is_valid_global_event_table_id(current_byte):
            return self.__handle_rca3_state(action_code=action_code, i=i + 1, f7_counter=f7_counter)
        elif sub_action_code is ActionCode.SET_STATS_OR_TOGGLE_STATUS and StatsAndPropertiesTable.is_valid_party_member_property_offset(self.__game_version, current_byte):
            return self.__handle_rca3_state(action_code=action_code, i=i + 1, f7_counter=f7_counter)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_rca3_state(self, action_code: ActionCode, i: int, f7_counter: int) -> bool:
        '''
        We just read either of the following:
        - A simple action byte (as part of a 4-byte random selection action).
        - The second byte of a 3-byte action (as part of a 4-byte AI command).

        The next byte must be one of the following:
        - A simple action byte (0x00-0xEF) if and only if the previous byte was a simple action byte (as part of a 4-byte random selection action).
        - The third byte of a 3-byte action otherwise (as part of a 4-byte AI command).
        '''
        self.__current_state = StateEnum.RCA3

        f7_counter = max(f7_counter - 1, -1)

        current_byte: int = self.__tokens[i]

        self.__current_tokens_group.append(current_byte)

        if action_code is ActionCode.GBA_RANDOM_SELECTION and Ability.is_valid_id(current_byte):
            return self.__handle_rca4_state(i=i + 1, f7_counter=f7_counter)
        elif action_code is ActionCode.RANDOM_SELECTION and Ability.is_valid_non_dark_arts_id(current_byte):
            return self.__handle_rca4_state(i=i + 1, f7_counter=f7_counter)
        elif action_code is ActionCode.AI_COMMAND:  # The last byte is unrestricted for 3-byte actions (as part of a 4-byte command).
            return self.__handle_rca4_state(i=i + 1, f7_counter=f7_counter)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_rca4_state(self, i: int, f7_counter: int) -> bool:
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

        self.__enemy_ai.add_action(tokens=self.__current_tokens_group, battle_text=self.__battle_text)

        if f7_counter == 0:
            # We found the last sub-action of a no-interrupt action whose length does not cover a separator or terminator byte.
            self.__enemy_ai.finalise_no_interrupt_action(additional_length=False)

        f7_counter = max(f7_counter - 1, -1)

        current_byte: int = self.__tokens[i]

        self.__current_tokens_group = [current_byte]

        # Because of some ID collisions, the order of the checks is critical here (i.e., Dark Arts abilities share the same IDs with some AI commands).
        # First, non-dark arts abilities must be checked, then complex action codes, and finally dark arts abilities.
        if Ability.is_valid_non_dark_arts_id(current_byte):
            return self.__handle_rsa_state(i=i + 1, f7_counter=f7_counter)
        elif ActionCode.is_valid_four_byte_action_code(current_byte):
            return self.__handle_rca1_state(action_code=ActionCode(current_byte), i=i + 1, f7_counter=f7_counter)
        elif DarkArts.is_valid_id(current_byte):
            return self.__handle_rsa_state(i=i + 1, f7_counter=f7_counter)
        elif current_byte is SymbolCode.SEPARATOR.value:
            return self.__handle_sep5_state(i=i + 1, f7_counter=f7_counter)
        elif current_byte is SymbolCode.TERMINATOR.value:
            return self.__handle_ter2_state(previous_byte=current_byte, i=i + 1, f7_counter=f7_counter)
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_sep5_state(self, i: int, f7_counter: int) -> bool:
        '''
        We just read a separator byte (0xFE) after an action block in the reactive AI.

        The next byte must be a reactive condition first byte (0x01-0x12).
        '''
        self.__current_state = StateEnum.SEP5

        if self.__enemy_ai.has_lingering_no_interrupt_action():
            # The separator that brought us here is covered by the length of a lingering no-interrupt action.
            self.__enemy_ai.finalise_no_interrupt_action(additional_length=True)

        self.__enemy_ai.add_separator(tokens=self.__current_tokens_group)

        f7_counter = max(f7_counter - 1, -1)

        current_byte: int = self.__tokens[i]

        self.__current_tokens_group = [current_byte]

        if ConditionCode.is_valid_condition_code(current_byte) and current_byte is not ConditionCode.UNCONDITIONAL.value:
            return self.__handle_rc1_state(condition_code=ConditionCode(current_byte), i=i + 1) 
        else:
            return self.__handle_error_state(previous_byte=current_byte)

    def __handle_ter2_state(self, previous_byte: int, i: int, f7_counter: int) -> bool:
        '''
        We finished parsing the reactive AI, and, therefore, the entire AI.
        '''
        self.__current_state = StateEnum.TER2

        if self.__enemy_ai.has_lingering_no_interrupt_action():
            # The terminator that brought us here is covered by the length of a lingering no-interrupt action.
            self.__enemy_ai.finalise_no_interrupt_action(additional_length=True, override_length_mismatch=True)

        self.__enemy_ai.add_terminator(tokens=self.__current_tokens_group)

        self.__current_tokens_group = []

        f7_counter = max(f7_counter - 1, -1)

        if f7_counter > 0:
            return self.__handle_error_state(previous_byte=previous_byte, optional_message="Not enough bytes were parsed after a NO_INTERRUPT action.")
        elif len(self.__tokens) != i:
            return self.__handle_error_state(previous_byte=previous_byte, optional_message="Extra bytes were found after parsing the entire AI.")
        else:
            return True
