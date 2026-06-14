from .enums.ability import Ability


class EnemyAITokeniser():
    @staticmethod
    def tokenise(enemy_id: str, hex_ai: str) -> list[list[int]]:
        if len(hex_ai) % 2 != 0:
            raise ValueError("Any hex string must have an even number of characters.")
        elif any(c not in "0123456789ABCDEF" for c in hex_ai.upper()):
            raise ValueError("Any hex string must only contain characters 0-9 and A-F.")
        else:
            raw_bytes: list[int] = [int(hex_ai[i:i+2], 16) for i in range(0, len(hex_ai), 2)]

            tokens: list[list[int]] = EnemyAITokeniser.__tokenise_raw_bytes(raw_bytes)

            EnemyAITokeniser.__validate_tokens(enemy_id, hex_ai.upper(), tokens)

            return tokens

    @staticmethod
    def detokenise(tokens: list[list[int]]) -> str:
        raw_bytes: list[int] = [byte for token in tokens for byte in token]

        return "".join(f"{byte:02X}" for byte in raw_bytes)

    @staticmethod
    def __validate_tokens(enemy_id: str, hex_ai: str, tokens: list[list[int]]) -> None:
        if EnemyAITokeniser.detokenise(tokens) != hex_ai:
            raise ValueError(f"Detokenised AI for enemy {enemy_id} does not match original hex AI.\nHex AI: {hex_ai}.\nDetokenised AI: {EnemyAITokeniser.detokenise(tokens)}.")

        for token in tokens:
            if len(token) == 1:
                if token[0] not in {0xFE, 0xFF} and token[0] not in {ability.value for ability in Ability}:
                    raise ValueError(f"Token {token} for enemy {enemy_id} is not a valid boundary or simple ability token.")
            elif len(token) == 4:
                if not (token[0] < 0x13 or 0xF1 < token[0] < 0xFE):
                    raise ValueError(f"Token {token} for enemy {enemy_id} has an invalid first byte: {token[0]:02X}.")
            else:
                raise ValueError(f"Token {token} for enemy {enemy_id} does not have a length of 1 or 4.")

    @staticmethod
    def __tokenise_raw_bytes(raw_bytes: list[int]) -> list[list[int]]:
        tokens: list[list[int]] = []
        current_token: list[int] = []
        simple_ability_tokens: set[int] = {ability.value for ability in Ability}
        boundary_bytes: set[int] = {0xFE, 0xFF}
        in_action_block: bool = False

        for byte in raw_bytes:
            if byte in boundary_bytes:
                current_token = EnemyAITokeniser.__handle_boundary_byte(byte=byte, tokens=tokens, current_token=current_token, in_action_block=in_action_block)
                in_action_block = not in_action_block
            elif in_action_block:
                current_token = EnemyAITokeniser.__handle_action_byte(byte=byte, tokens=tokens, current_token=current_token, simple_ability_tokens=simple_ability_tokens)
            else:
                current_token = EnemyAITokeniser.__handle_condition_byte(byte=byte, tokens=tokens, current_token=current_token)

        if current_token:
            raise ValueError(f"Unexpected end of raw bytes while tokenising. Current token: {current_token}. Tokens: {tokens}. In action block: {in_action_block}.")

        return tokens

    @staticmethod
    def __handle_boundary_byte(byte: int, tokens: list[list[int]], current_token: list[int], in_action_block: bool) -> list[int]:
        if len(current_token) == 4:
            tokens.append(current_token)
            tokens.append([byte])

            return []
        elif current_token:
            raise ValueError(f"Unexpected boundary byte {byte:02X} while tokenising. Current token: {current_token}. Tokens: {tokens}. In action block: {in_action_block}.")
        else:
            tokens.append([byte])

            return []

    @staticmethod
    def __handle_condition_byte(byte: int, tokens: list[list[int]], current_token: list[int]) -> list[int]:
        if len(current_token) == 4:
            tokens.append(current_token)

            return [byte]
        else:
            current_token.append(byte)

            return current_token

    @staticmethod
    def __handle_action_byte(byte: int, tokens: list[list[int]], current_token: list[int], simple_ability_tokens: set[int]) -> list[int]:
        is_simple_action: bool = byte in simple_ability_tokens

        if not current_token and is_simple_action:
            tokens.append([byte])

            return []
        elif len(current_token) == 4 and is_simple_action:
            tokens.append(current_token)
            tokens.append([byte])

            return []
        elif len(current_token) == 4:
            tokens.append(current_token)

            return [byte]
        else:
            current_token.append(byte)

            return current_token
