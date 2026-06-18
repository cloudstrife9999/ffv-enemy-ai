#!/usr/bin/env python3

from __future__ import annotations

from json import dump, load
from pathlib import Path
from typing import Any, TypeAlias

from parser.parser import EnemyAIParser

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


def convert_battle_text_keys_to_int(battle_text: dict[str, dict[str, str]]) -> dict[int, dict[int, str]]:
    converted_battle_text: dict[int, dict[int, str]] = {}

    for table_number_str, entries in battle_text.items():
        table_number: int = int(table_number_str)
        converted_entries: dict[int, str] = {int(entry_number_str): message for entry_number_str, message in entries.items()}

        converted_battle_text[table_number] = converted_entries

    return converted_battle_text


def parse_enemy_ai(enemy_id: str, enemy_name: str, hex_ai: str, battle_text: dict[int, dict[int, str]]) -> tuple[bool, EnemyAIParser]:
    parser: EnemyAIParser = EnemyAIParser(enemy_id=enemy_id, enemy_name=enemy_name, tokens=bytes.fromhex(hex_ai), battle_text=battle_text)

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


def parse_with_optional_patch(enemy_id: str, enemy_name: str, hex_ai: str, battle_text: dict[int, dict[int, str]]) -> tuple[bool, str, EnemyAIParser]:
    valid, parser = parse_enemy_ai(enemy_id, enemy_name, hex_ai, battle_text)

    if valid or enemy_id != PATCHED_ENEMY_ID:
        return valid, hex_ai, parser

    patched_hex_ai: str = patch_hex_ai(enemy_id, hex_ai)
    valid, parser = parse_enemy_ai(enemy_id, enemy_name, patched_hex_ai, battle_text)

    return valid, patched_hex_ai, parser


def validate_recompile(enemy_id: str, hex_ai: str, parser: EnemyAIParser) -> None:
    recompiled: str = parser.recompile_tokens()

    if recompiled != hex_ai:
        raise ValueError(f"[Parser] Parsed and recompiled AI for enemy {enemy_id} does not match original hex AI.\nHex AI: {hex_ai}.\nRecompiled AI: {recompiled}.")


def parse_ai(enemy_id: str, enemy_name: str, original_hex_ai: str, battle_text: dict[int, dict[int, str]]) -> tuple[JsonObject, list[str]]:
    valid, final_hex_ai, parser = parse_with_optional_patch(enemy_id, enemy_name, original_hex_ai, battle_text)

    if not valid:
        error: str = (f"Failed to parse AI even after patching {BAD_TERMINATOR} to {GOOD_TERMINATOR}." if enemy_id == PATCHED_ENEMY_ID else "Failed to parse AI.")

        return failure_result(enemy_id, enemy_name, final_hex_ai, error), []

    validate_recompile(enemy_id, final_hex_ai, parser)

    parsed_ai: JsonObject = parser.get_parsed_ai().to_json()
    ai_script: list[str] = parser.get_parsed_ai().to_compact_representation()

    if final_hex_ai != original_hex_ai:
        parsed_ai["raw"] = final_hex_ai

    return parsed_ai, ai_script


def generate_and_write_validation_results(enemy_ai_map: dict[str, str], enemy_names: dict[str, str], battle_text: dict[int, dict[int, str]]) -> list[list[str]]:
    parsed_ai_list: list[JsonObject] = []
    ai_script_list: list[list[str]] = []
    
    for enemy_id, hex_ai in enemy_ai_map.items():
        enemy_name: str = enemy_names.get(enemy_id, "Unknown Enemy")
        parsed_ai, ai_script = parse_ai(enemy_id, enemy_name, hex_ai, battle_text)

        parsed_ai_list.append(parsed_ai)
        ai_script_list.append(ai_script)

    write_json(Path(CONFIG["parsed_ai_file_path"]), parsed_ai_list)

    return ai_script_list


def write_ai_script(ai_script_list: list[list[str]], enemy_names: dict[str, str]) -> None:
    ai_script_lines: list[str] = []

    for (enemy_id, enemy_name), ai_script in zip(enemy_names.items(), ai_script_list):
        ai_script_lines.append(f"Enemy ID: {enemy_id}")
        ai_script_lines.append(f"Enemy Name: {enemy_name}")

        for line in ai_script:
            ai_script_lines.append(line)

        ai_script_lines.append("\n" + "-" * 40 + "\n")

    write_compact_representation(Path(CONFIG["ai_script_representation_file_path"]), ai_script_lines)


def main() -> None:
    load_config()

    enemy_ai_map: dict[str, str] = load_json(Path(CONFIG["enemy_ai_map_file_path"]))
    enemy_names: dict[str, str] = load_json(Path(CONFIG["enemy_names_file_path"]))
    battle_text: dict[str, dict[str, str]] = load_json(Path(CONFIG["rpge_battle_text_file_path"]))
    converted_battle_text: dict[int, dict[int, str]] = convert_battle_text_keys_to_int(battle_text)

    ai_script_list: list[list[str]] = generate_and_write_validation_results(enemy_ai_map, enemy_names, converted_battle_text)
    
    write_ai_script(ai_script_list, enemy_names)


if __name__ == "__main__":
    main()
