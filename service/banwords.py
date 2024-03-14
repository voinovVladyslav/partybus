from pathlib import Path


def load_banwords(file_path: Path) -> set[str]:
    with open(file_path, 'r') as file:
        return set([line.strip().lower() for line in file.readlines()])


def is_banword(word: str, banwords: list[str]) -> bool:
    for banword in banwords:
        if banword in word:
            return True
    return False
