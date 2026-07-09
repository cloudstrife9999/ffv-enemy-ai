from abc import ABC, abstractmethod
from collections.abc import Mapping
from json import load, dump
from pathlib import Path
from typing import Any, TypeAlias

from .enums.abilities.special import Special
from .enums.game_version import GameVersion
from .parser import EnemyAIParser


JsonObject: TypeAlias = dict[str, Any]
JsonObjectWithIntegerKeys: TypeAlias = dict[int, Any]


class AbstractAIParser(ABC):
    CONFIG_FILE_PATH: Path = Path("res/config.json")
    __PATCHED_ENEMY_ID: str = "E5"
    __BAD_TERMINATOR: str = "FEFF"
    __GOOD_TERMINATOR: str = "FFFF"

    def __init__(self, game_version: GameVersion, write_individual_ai_scripts: bool=False) -> None:
        self.__config: dict[str, str] = self.load_config()
        self.__game_version: GameVersion = game_version
        self.__write_individual_ai_scripts: bool = write_individual_ai_scripts

        self.__enemy_ai_map: dict[str, str] = {}
        self.__enemy_names: dict[str, str] = {}
        self.__enemy_special_abilities: dict[int, dict[str, int]] = {}
        self.__battle_text: dict[int, str] = {}

        self.__ai_output_path: Path = Path(self.__config["parsed_ai_file_path"])
        self.__script_output_path: Path = Path(self.__config["ai_script_representation_file_path"])
        self.__individual_ai_output_dir: Path = Path(self.__config["individual_ai_output_dir"])

    @property
    def config(self) -> Mapping[str, str]:
        return self.__config

    @abstractmethod
    def load_config(self) -> dict[str, str]:
        """Load configuration and normalize subclass-specific key names."""
        ...

    def run(self) -> None:
        self._load_resources()

        ai_script_list: list[list[str]] = self.generate_and_write_validation_results()

        self.write_ai_script(ai_script_list)

        if self.__write_individual_ai_scripts:
                self.write_single_enemies_ai_script(ai_script_list)

    @staticmethod
    def load_and_normalise_config(bad_prefix: str, good_prefix: str) -> dict[str, str]:
        with AbstractAIParser.CONFIG_FILE_PATH.open("r", encoding="utf-8") as file:
            tmp_config: dict[str, str] = load(file)

        keys_to_remove: list[str] = [key for key in tmp_config if key.startswith(bad_prefix)]
        keys_to_rename: list[str] = [key for key in tmp_config if key.startswith(good_prefix)]

        for key in keys_to_remove:
            del tmp_config[key]

        for key in keys_to_rename:
            renamed_key: str = key.replace(good_prefix, "")

            tmp_config[renamed_key] = tmp_config[key]

            del tmp_config[key]

        return tmp_config

    def _load_resources(self) -> None:
        self.__enemy_ai_map = self.load_json(Path(self.__config["enemy_ai_map_file_path"]))
        self.__enemy_names = self.load_json(Path(self.__config["enemy_names_file_path"]))

        enemy_special_abilities: dict[str, str] = self.load_json(Path(self.__config["enemy_special_abilities_file_path"]))

        self.__enemy_special_abilities = self.convert_enemy_special_abilities_keys_to_int(enemy_special_abilities)

        battle_text: dict[str, str] = self.load_json(Path(self.__config["battle_text_file_path"]))
        self.__battle_text = self.convert_battle_text_keys_to_int(battle_text)

    @staticmethod
    def load_json(path: Path) -> JsonObject:
        with path.open("r", encoding="utf-8") as file:
            return load(file)

    @staticmethod
    def write_json(path: Path, data: Any) -> None:
        with path.open("w", encoding="utf-8") as file:
            dump(data, file, indent=4, ensure_ascii=False)

    @staticmethod
    def write_individual_json_ai_scripts(output_dir: Path, enemy_name: str, parsed_ai: JsonObject) -> None:
        output_path: Path = output_dir / "json_data" / f"{enemy_name}.json"

        AbstractAIParser.write_json(output_path, parsed_ai)

    @staticmethod
    def write_compact_representation(path: Path, lines: list[str]) -> None:
        with path.open("w", encoding="utf-8") as file:
            for line in lines:
                file.write(line + "\n")

    @staticmethod
    def convert_enemy_special_abilities_keys_to_int(enemy_special_abilities: dict[str, str]) -> dict[int, dict[str, int]]:
        converted_enemy_special_abilities: dict[int, dict[str, int]] = {}

        for enemy_id_str, data in enemy_special_abilities.items():
            enemy_id: int = int(enemy_id_str, 16)
            raw_flags: str = data[:2]
            raw_id: str = data[2:]

            converted_enemy_special_abilities[enemy_id] = {
                "special_ability_flags": int(raw_flags, 16) if raw_flags else -1,
                "special_ability_id": int(raw_id, 16) if raw_id else -1,
            }

        return converted_enemy_special_abilities

    @staticmethod
    def convert_battle_text_keys_to_int(battle_text: dict[str, str]) -> dict[int, str]:
        converted_battle_text: dict[int, str] = {}

        for key, value in battle_text.items():
            table_number: int = int(key, 16)
            converted_battle_text[table_number] = value

        return converted_battle_text

    def generate_and_write_validation_results(self) -> list[list[str]]:
        parsed_ai_list: list[JsonObject] = []
        ai_script_list: list[list[str]] = []

        for enemy_id, hex_ai in self.__enemy_ai_map.items():
            enemy_name: str = self.__enemy_names.get(enemy_id, "Unknown Enemy")
            enemy_special_ability_id: int = self.__enemy_special_abilities.get(int(enemy_id, 16), {}).get("special_ability_id", -1)
            enemy_special_ability: str = str(Special(enemy_special_ability_id)) if enemy_special_ability_id != -1 else "[special ability]"
            parsed_ai, ai_script = self.parse_ai(enemy_id, enemy_name, enemy_special_ability, hex_ai)

            parsed_ai_list.append(parsed_ai)
            ai_script_list.append(ai_script)

            if self.__write_individual_ai_scripts:
                AbstractAIParser.write_individual_json_ai_scripts(self.__individual_ai_output_dir, enemy_name, parsed_ai)

        self.write_json(self.__ai_output_path, parsed_ai_list)

        return ai_script_list

    def parse_ai(self, enemy_id: str, enemy_name: str, enemy_special_ability: str, original_hex_ai: str) -> tuple[JsonObject, list[str]]:
        valid, final_hex_ai, parser = self.parse_with_optional_patch(enemy_id, enemy_name, enemy_special_ability, original_hex_ai)

        if not valid:
            error: str = f"Failed to parse AI even after patching {self.__BAD_TERMINATOR} to {self.__GOOD_TERMINATOR}." if enemy_id == self.__PATCHED_ENEMY_ID else "Failed to parse AI."

            return self.failure_result(enemy_id, enemy_name, final_hex_ai, error), []

        self.validate_recompile(enemy_id, final_hex_ai, parser)

        parsed_ai: JsonObject = parser.get_parsed_ai().to_json()
        ai_script: list[str] = parser.get_parsed_ai().to_compact_representation()

        if final_hex_ai != original_hex_ai:
            parsed_ai["raw"] = final_hex_ai

        return parsed_ai, ai_script

    def parse_with_optional_patch(self, enemy_id: str, enemy_name: str, enemy_special_ability: str, hex_ai: str) -> tuple[bool, str, EnemyAIParser]:
        valid, parser = self.parse_enemy_ai(enemy_id, enemy_name, enemy_special_ability, hex_ai)

        if valid or enemy_id != self.__PATCHED_ENEMY_ID:
            return valid, hex_ai, parser

        patched_hex_ai: str = self.patch_hex_ai(enemy_id, hex_ai)
        valid, parser = self.parse_enemy_ai(enemy_id, enemy_name, enemy_special_ability, patched_hex_ai)

        return valid, patched_hex_ai, parser

    @classmethod
    def patch_hex_ai(cls, enemy_id: str, hex_ai: str) -> str:
        if enemy_id != cls.__PATCHED_ENEMY_ID:
            return hex_ai

        return hex_ai.replace(cls.__BAD_TERMINATOR, cls.__GOOD_TERMINATOR)

    @staticmethod
    def validate_recompile(enemy_id: str, hex_ai: str, parser: EnemyAIParser) -> None:
        recompiled: str = parser.recompile_tokens()

        if recompiled != hex_ai:
            raise ValueError(f"[Parser] Parsed and recompiled AI for enemy {enemy_id} does not match original hex AI.\nHex AI: {hex_ai}.\nRecompiled AI: {recompiled}.")

    @staticmethod
    def failure_result(enemy_id: str, enemy_name: str, hex_ai: str, error: str) -> JsonObject:
        return {
            "enemy_id": enemy_id,
            "enemy_name": enemy_name,
            "valid": False,
            "raw": hex_ai,
            "error": error,
        }

    def parse_enemy_ai(self, enemy_id: str, enemy_name: str, enemy_special_ability: str, hex_ai: str) -> tuple[bool, EnemyAIParser]:
        parser: EnemyAIParser = EnemyAIParser(enemy_id=enemy_id, enemy_name=enemy_name, enemy_special_ability=enemy_special_ability, tokens=bytes.fromhex(hex_ai), battle_text=self.__battle_text, game_version=self.__game_version)

        return parser.parse(), parser

    def write_ai_script(self, ai_script_list: list[list[str]]) -> None:
        ai_script_lines: list[str] = []

        for (enemy_id, enemy_name), ai_script in zip(self.__enemy_names.items(), ai_script_list):
            ai_script_lines.append(f"Enemy ID: {enemy_id}")
            ai_script_lines.append(f"Enemy Name: {enemy_name}")

            for line in ai_script:
                ai_script_lines.append(line)

            ai_script_lines.append("\n" + "-" * 40 + "\n")

        self.write_compact_representation(self.__script_output_path, ai_script_lines)

    def write_single_enemies_ai_script(self, ai_script_list: list[list[str]]) -> None:
        output_dir: Path = self.__individual_ai_output_dir / "wikitext"
        output_dir.mkdir(parents=True, exist_ok=True)

        for enemy_id, enemy_name in self.__enemy_names.items():
            ai_script: list[str] = ai_script_list[list(self.__enemy_names.keys()).index(enemy_id)]
            ai_script_lines: list[str] = [
                "==[[Final Fantasy V enemy AI|AI script]]==",
                "<pre style=\"white-space: pre; overflow-x: auto; max-width: 100%;\">"
            ]

            for line in ai_script:
                ai_script_lines.append(line)

            ai_script_lines.append("</pre>")

            output_file_path: Path = output_dir / f"{enemy_name}.wikitext"

            AbstractAIParser.write_compact_representation(output_file_path, ai_script_lines)
