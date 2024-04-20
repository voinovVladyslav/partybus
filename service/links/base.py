import re
from copy import deepcopy


class Linker:
    def __init__(self, patterns: list[dict]):
        self.patterns = deepcopy(patterns)
        self.filter_patterns()

    def filter_patterns(self) -> None:
        pass

    def render(self, text: str) -> str:
        for pattern in self.patterns:
            link = r'<a href="{}">\1</a>'.format(pattern['link'])
            keywords = '|'.join(pattern['keywords'])
            regex = re.compile(fr'({keywords})', re.IGNORECASE)
            text = regex.sub(link, text)
        return text
