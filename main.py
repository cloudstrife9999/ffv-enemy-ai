#!/usr/bin/env python3

from __future__ import annotations

from json import dump, load
from pathlib import Path
from typing import Any, TypeAlias

from parser.parser import EnemyAIParser

# TODO: move these constants to a config file.
ENEMY_AI_MAP_PATH: Path = Path("res/enemies/enemy_ai_map.json")
ENEMY_NAMES_PATH: Path = Path("res/enemies/enemy_names.json")
OUTPUT_PATH: Path = Path("res/enemies/parsed_ai.json")

PATCHED_ENEMY_ID: str = "E5"
BAD_TERMINATOR: str = "FEFF"
GOOD_TERMINATOR: str = "FFFF"


JsonObject: TypeAlias = dict[str, Any]


def load_json(path: Path) -> JsonObject:
    with path.open("r", encoding="utf-8") as file:
        return load(file)


def write_json(path: Path, data: Any) -> None:
    with path.open("w", encoding="utf-8") as file:
        dump(data, file, indent=4)


def parse_enemy_ai(enemy_id: str, enemy_name: str, hex_ai: str) -> tuple[bool, EnemyAIParser]:
    parser: EnemyAIParser = EnemyAIParser(enemy_id=enemy_id, enemy_name=enemy_name, tokens=bytes.fromhex(hex_ai))

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


def parse_with_optional_patch(enemy_id: str, enemy_name: str, hex_ai: str) -> tuple[bool, str, EnemyAIParser]:
    valid, parser = parse_enemy_ai(enemy_id, enemy_name, hex_ai)

    if valid or enemy_id != PATCHED_ENEMY_ID:
        return valid, hex_ai, parser

    patched_hex_ai: str = patch_hex_ai(enemy_id, hex_ai)
    valid, parser = parse_enemy_ai(enemy_id, enemy_name, patched_hex_ai)

    return valid, patched_hex_ai, parser


def validate_recompile(enemy_id: str, hex_ai: str, parser: EnemyAIParser) -> None:
    recompiled: str = parser.recompile_tokens()

    if recompiled != hex_ai:
        raise ValueError(f"[Parser] Parsed and recompiled AI for enemy {enemy_id} does not match original hex AI.\nHex AI: {hex_ai}.\nRecompiled AI: {recompiled}.")


def build_validation_result(enemy_id: str, enemy_name: str, original_hex_ai: str) -> JsonObject:
    valid, final_hex_ai, parser = parse_with_optional_patch(enemy_id, enemy_name, original_hex_ai)

    if not valid:
        error: str = (f"Failed to parse AI even after patching {BAD_TERMINATOR} to {GOOD_TERMINATOR}." if enemy_id == PATCHED_ENEMY_ID else "Failed to parse AI.")

        return failure_result(enemy_id, enemy_name, final_hex_ai, error)

    validate_recompile(enemy_id, final_hex_ai, parser)

    result: JsonObject = parser.get_parsed_ai().to_json()

    if final_hex_ai != original_hex_ai:
        result["raw"] = final_hex_ai

    return result


def main() -> None:
    enemy_ai_map: dict[str, str] = load_json(ENEMY_AI_MAP_PATH)
    enemy_names: dict[str, str] = load_json(ENEMY_NAMES_PATH)

    validation_results: list[JsonObject] = [build_validation_result(enemy_id, enemy_names[enemy_id], hex_ai) for enemy_id, hex_ai in enemy_ai_map.items()]

    write_json(OUTPUT_PATH, validation_results)


if __name__ == "__main__":
    main()
