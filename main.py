#!/usr/bin/env python3

from __future__ import annotations

from json import dump, load
from pathlib import Path
from typing import Any, TypeAlias

from parser.parser import EnemyAIParser
from parser.enums.abilities.special import Special
from parser.enums.game_version import GameVersion

CONFIG_FILE_PATH: Path = Path("res/config.json")
CONFIG: dict[str, str] = {}

PATCHED_ENEMY_ID: str = "E5"
BAD_TERMINATOR: str = "FEFF"
GOOD_TERMINATOR: str = "FFFF"


JsonObject: TypeAlias = dict[str, Any]
JsonObjectWithIntegerKeys: TypeAlias = dict[int, Any]


def load_config() -> None:
    with CONFIG_FILE_PATH.open("r", encoding="utf-8") as file:
        config: dict[str, str] = load(file)

        CONFIG.update(config)   
        

def load_json(path: Path) -> JsonObject:
    with path.open("r", encoding="utf-8") as file:
        return load(file)


def write_json(path: Path, data: Any) -> None:
    with path.open("w", encoding="utf-8") as file:
        dump(data, file, indent=4)


def write_compact_representation(path: Path, lines: list[str]) -> None:
    with path.open("w", encoding="utf-8") as file:
        for line in lines:
            file.write(line + "\n")


def convert_battle_text_keys_to_int(battle_text: dict[str, str]) -> dict[int, str]:
    converted_battle_text: dict[int, str] = {}

    for key, value in battle_text.items():
        table_number: int = int(key, 16)

        converted_battle_text[table_number] = value

    return converted_battle_text

def convert_enemy_special_abilities_keys_to_int(enemy_special_abilities: dict[str, str]) -> dict[int, dict[str, int]]:
    converted_enemy_special_abilities: dict[int, dict[str, int]] = {}
    for enemy_id_str, data in enemy_special_abilities.items():
        enemy_id: int = int(enemy_id_str, 16)
        raw_flags: str = data[:2]
        raw_id: str = data[2:]

        converted_enemy_special_abilities[enemy_id] = {
            "special_ability_flags": int(raw_flags, 16) if raw_flags else -1,
            "special_ability_id": int(raw_id, 16) if raw_id else -1
        }

    return converted_enemy_special_abilities


def parse_enemy_ai(game_version: GameVersion, enemy_id: str, enemy_name: str, enemy_special_ability: str, hex_ai: str, battle_text: dict[int, str]) -> tuple[bool, EnemyAIParser]:
    parser: EnemyAIParser = EnemyAIParser(enemy_id=enemy_id, enemy_name=enemy_name, enemy_special_ability=enemy_special_ability, tokens=bytes.fromhex(hex_ai), battle_text=battle_text, game_version=game_version)

    return parser.parse(), parser


def failure_result(enemy_id: str, enemy_name: str, hex_ai: str, error: str) -> JsonObject:
    return {
        "enemy_id": enemy_id,
        "enemy_name": enemy_name,
        "valid": False,
        "raw": hex_ai,
        "error": error,
    }


def patch_hex_ai(enemy_id: str, hex_ai: str) -> str:
    if enemy_id != PATCHED_ENEMY_ID:
        return hex_ai
    else:
        return hex_ai.replace(BAD_TERMINATOR, GOOD_TERMINATOR)


def parse_with_optional_patch(game_version: GameVersion, enemy_id: str, enemy_name: str, enemy_special_ability: str, hex_ai: str, battle_text: dict[int, str]) -> tuple[bool, str, EnemyAIParser]:
    valid, parser = parse_enemy_ai(game_version, enemy_id, enemy_name, enemy_special_ability, hex_ai, battle_text)

    if valid or enemy_id != PATCHED_ENEMY_ID:
        return valid, hex_ai, parser

    patched_hex_ai: str = patch_hex_ai(enemy_id, hex_ai)
    valid, parser = parse_enemy_ai(game_version, enemy_id, enemy_name, enemy_special_ability, patched_hex_ai, battle_text)

    return valid, patched_hex_ai, parser


def validate_recompile(enemy_id: str, hex_ai: str, parser: EnemyAIParser) -> None:
    recompiled: str = parser.recompile_tokens()

    if recompiled != hex_ai:
        raise ValueError(f"[Parser] Parsed and recompiled AI for enemy {enemy_id} does not match original hex AI.\nHex AI: {hex_ai}.\nRecompiled AI: {recompiled}.")


def parse_ai(game_version: GameVersion, enemy_id: str, enemy_name: str, enemy_special_ability: str, original_hex_ai: str, battle_text: dict[int, str]) -> tuple[JsonObject, list[str]]:
    valid, final_hex_ai, parser = parse_with_optional_patch(game_version, enemy_id, enemy_name, enemy_special_ability, original_hex_ai, battle_text)

    if not valid:
        error: str = (f"Failed to parse AI even after patching {BAD_TERMINATOR} to {GOOD_TERMINATOR}." if enemy_id == PATCHED_ENEMY_ID else "Failed to parse AI.")

        return failure_result(enemy_id, enemy_name, final_hex_ai, error), []

    validate_recompile(enemy_id, final_hex_ai, parser)

    parsed_ai: JsonObject = parser.get_parsed_ai().to_json()
    ai_script: list[str] = parser.get_parsed_ai().to_compact_representation()

    if final_hex_ai != original_hex_ai:
        parsed_ai["raw"] = final_hex_ai

    return parsed_ai, ai_script


def generate_and_write_validation_results(game_version: GameVersion, enemy_ai_map: dict[str, str], enemy_names: dict[str, str], converted_enemy_special_abilities: dict[int, dict[str, int]], battle_text: dict[int, str], ai_output_file: str) -> list[list[str]]:
    parsed_ai_list: list[JsonObject] = []
    ai_script_list: list[list[str]] = []
    
    for enemy_id, hex_ai in enemy_ai_map.items():
        enemy_name: str = enemy_names.get(enemy_id, "Unknown Enemy")
        enemy_special_ability_id: int = converted_enemy_special_abilities.get(int(enemy_id, 16), {}).get("special_ability_id", -1)
        enemy_special_ability: str = str(Special(enemy_special_ability_id)) if enemy_special_ability_id != -1 else "[special ability]"
        parsed_ai, ai_script = parse_ai(game_version, enemy_id, enemy_name, enemy_special_ability, hex_ai, battle_text)

        parsed_ai_list.append(parsed_ai)
        ai_script_list.append(ai_script)

    write_json(Path(ai_output_file), parsed_ai_list)

    return ai_script_list


def write_ai_script(ai_script_list: list[list[str]], enemy_names: dict[str, str], script_output_file: str) -> None:
    ai_script_lines: list[str] = []

    for (enemy_id, enemy_name), ai_script in zip(enemy_names.items(), ai_script_list):
        ai_script_lines.append(f"Enemy ID: {enemy_id}")
        ai_script_lines.append(f"Enemy Name: {enemy_name}")

        for line in ai_script:
            ai_script_lines.append(line)

        ai_script_lines.append("\n" + "-" * 40 + "\n")

    write_compact_representation(Path(script_output_file), ai_script_lines)


def snes_main() -> None:
    enemy_ai_map: dict[str, str] = load_json(Path(CONFIG["enemy_ai_map_file_path"]))
    enemy_names: dict[str, str] = load_json(Path(CONFIG["enemy_names_file_path"]))
    enemy_special_abilities: dict[str, str] = load_json(Path(CONFIG["enemy_special_abilities_file_path"]))
    converted_enemy_special_abilities: dict[int, dict[str, int]] = convert_enemy_special_abilities_keys_to_int(enemy_special_abilities)
    battle_text: dict[str, str] = load_json(Path(CONFIG["rpge_battle_text_file_path"]))
    converted_battle_text: dict[int, str] = convert_battle_text_keys_to_int(battle_text)
    ai_output_file: str = CONFIG["parsed_ai_file_path"]
    script_output_file: str = CONFIG["ai_script_representation_file_path"]

    ai_script_list: list[list[str]] = generate_and_write_validation_results(GameVersion.SNES, enemy_ai_map, enemy_names, converted_enemy_special_abilities, converted_battle_text, ai_output_file)
    
    write_ai_script(ai_script_list, enemy_names, script_output_file)


def gba_main() -> None:
    enemy_ai_map: dict[str, str] = load_json(Path(CONFIG["gba_enemy_ai_map_file_path"]))
    enemy_names: dict[str, str] = load_json(Path(CONFIG["gba_enemy_names_file_path"]))
    enemy_special_abilities: dict[str, str] = load_json(Path(CONFIG["gba_enemy_special_abilities_file_path"]))
    converted_enemy_special_abilities: dict[int, dict[str, int]] = convert_enemy_special_abilities_keys_to_int(enemy_special_abilities)
    battle_text: dict[str, str] = load_json(Path(CONFIG["gba_battle_text_file_path"]))
    converted_battle_text: dict[int, str] = convert_battle_text_keys_to_int(battle_text)
    ai_output_file: str = CONFIG["gba_parsed_ai_file_path"]
    script_output_file: str = CONFIG["gba_ai_script_representation_file_path"]

    ai_script_list: list[list[str]] = generate_and_write_validation_results(GameVersion.GBA, enemy_ai_map, enemy_names, converted_enemy_special_abilities, converted_battle_text, ai_output_file)
    
    write_ai_script(ai_script_list, enemy_names, script_output_file)


def main() -> None:
    load_config()

    snes_main()
    gba_main()


if __name__ == "__main__":
    main()
