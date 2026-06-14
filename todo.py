#!/usr/bin/env python3

from pathlib import Path

TODO_MARKER = "TODO: "
ROOT = Path(".")
OUTPUT_FILE = Path("TODO.md")

ALLOWED_EXTENSIONS = {".py"}
EXCLUDE_DIRS = {"old", "venv", "__pycache__"}
EXCLUDE_FILES = {"todo.py"}


type Todo = tuple[int, str]
type TodosByFile = dict[Path, list[Todo]]


def should_skip_dir(path: Path) -> bool:
    return any(part in EXCLUDE_DIRS for part in path.parts)


def should_scan_file(path: Path) -> bool:
    return path.suffix in ALLOWED_EXTENSIONS and path.name not in EXCLUDE_FILES


def find_todos_in_file(path: Path) -> list[Todo]:
    todos: list[Todo] = []

    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if TODO_MARKER in line:
                todos.append((line_number, line.strip()))

    return todos


def collect_todos(root: Path) -> TodosByFile:
    todos_by_file: TodosByFile = {}

    for path in root.rglob("*.py"):
        if should_skip_dir(path) or not should_scan_file(path):
            continue

        todos: list[Todo] = find_todos_in_file(path)

        if todos:
            todos_by_file[path] = todos

    return todos_by_file


def write_todo_markdown(todos_by_file: TodosByFile, output_file: Path) -> None:
    lines: list[str] = ["# TODO List", ""]

    for file_path, todos in todos_by_file.items():
        lines.append(f"## [{file_path}]({file_path})")
        lines.append("")

        for line_number, todo_text in todos:
            lines.append(f"- Line {line_number}: {todo_text}")

        lines.append("")

    output_file.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    todos_by_file: TodosByFile = collect_todos(ROOT)

    write_todo_markdown(todos_by_file, OUTPUT_FILE)


if __name__ == "__main__":
    main()
