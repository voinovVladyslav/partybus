def is_banword(word: str, banwords: list[str]) -> bool:
    for banword in banwords:
        if word.startswith(banword):
            return True
    return False
