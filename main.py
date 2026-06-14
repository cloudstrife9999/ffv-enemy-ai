#!/usr/bin/env python3

from json import load, dump
from typing import Any

from parser.ai_factory import EnemyAIFactory
from parser.enemy_ai import EnemyAI


def main() -> None:
    enemy_ai_file: str = "res/enemies/enemy_ai_map.json"
    enemy_names_file: str = "res/enemies/enemy_names.json"
    output_file: str = "res/enemies/enemy_ai.json"
    parsed_enemy_ai: list[dict[str, Any]] = []

    with open(enemy_ai_file, "r") as f:
        enemy_ai_map: dict[str, str] = load(f)

    with open(enemy_names_file, "r") as f:
        enemy_names: dict[str, str] = load(f)

    for enemy_id, hex_ai in enemy_ai_map.items():
        if enemy_id not in enemy_names:
            raise ValueError(f"Enemy ID {enemy_id} is missing from the enemy names file.")
        else:
            enemy_name: str = enemy_names[enemy_id]
            enemy_ai: EnemyAI = EnemyAIFactory.create_ai(enemy_id=enemy_id, enemy_name=enemy_name, hex_ai=hex_ai)

            parsed_enemy_ai.append(enemy_ai.to_json())

    with open(output_file, "w") as f:
        dump(parsed_enemy_ai, f, indent=4)


if __name__ == "__main__":
    main()
