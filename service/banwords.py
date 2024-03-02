from pathlib import Path


def load_banwords(file_path: Path) -> list[str]:
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]


def is_banword(word: str, banwords: list[str]) -> bool:
    for banword in banwords:
        if word.startswith(banword):
            return True
    return False
