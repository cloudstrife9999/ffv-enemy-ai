#!/usr/bin/env python3

from json import load, dump

from parser.parser import StateMachine


if __name__ == "__main__":
    with open("res/enemies/enemy_ai_map.json", "r") as f:
        data: dict[str, str] = load(f)

    validation_results: list[dict[str, str | bool]] = []

    for enemy_id, hex_ai in data.items():
        tokens: bytes = bytes.fromhex(hex_ai)
        state_machine: StateMachine = StateMachine(tokens=tokens)
        valid: bool = state_machine.parse()

        validation_results.append({
            "enemy_id": enemy_id,
            "hex_ai": hex_ai,
            "valid": valid
        })

    with open("res/enemies/validation_results.json", "w") as f:
        dump(validation_results, f, indent=4)
