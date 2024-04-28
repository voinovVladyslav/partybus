import regex as re
from copy import deepcopy


class Linker:
    def __init__(
        self,
        patterns: list[dict],
        **kwargs
    ):
        self.kwargs = kwargs
        self.patterns = deepcopy(patterns)
        self.matched_links = set()
        self.filter_patterns()
        self.filter_current_city()

    def filter_patterns(self) -> None:
        pass

    def filter_current_city(self) -> None:
        city = self.kwargs.get('city_name')
        if not city:
            return

        for pattern in self.patterns:
            if pattern['header'] not in [
                'city_party_bus', 'city_charter_bus', 'home_page'
            ]:
                continue
            pattern['keywords'] = [
                w for w in pattern['keywords']
                if city.lower() not in w.lower()
            ]

    def render(self, text: str) -> str:
        for pattern in self.patterns:
            if pattern['link'] in self.matched_links:
                continue
            link = r'<a href="{}">\1</a>'.format(pattern['link'])
            keywords = '|'.join([
                fr'(?<!\">|"\/|")\b{w}\b(?!<\/a>|\/"|")'
                for w in pattern['keywords']
            ])
            if not keywords:
                continue

            regex = re.compile(fr'({keywords})', re.IGNORECASE)
            text, n = regex.subn(link, text, count=1)

            if n:
                self.matched_links.add(pattern['link'])

        return text
