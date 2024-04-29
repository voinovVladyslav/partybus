import regex as re
from copy import deepcopy


class Linker:
    def __init__(
        self,
        patterns: list[dict],
        **kwargs
    ):
        self.links_replaced = 0
        self.kwargs = kwargs
        self.patterns = deepcopy(patterns)
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

    def render(self, rows: list[dict[str, str]]) -> list[dict[str, str]]:
        for pattern in self.patterns:
            link = r'<a href="{}">\1</a>'.format(pattern['link'])
            keywords = '|'.join([
                fr'(?<!\">|"\/|"|\/a>\s?)\b{w}\b(?!<\/a>|\/"|"|\s?<a)'
                if not w.isdigit() else
                fr'(?<!\">|"\/|"|\/a>\s?)\b{w}\b(?!<\/a>|\/"|"|\s?<a|\s?second)'  # noqa
                for w in pattern['keywords']

            ])
            if not keywords:
                continue
            regex = re.compile(fr'({keywords})', re.IGNORECASE)

            biggest_match_len = 0
            match_idx = None
            for i, row in enumerate(rows):
                match = regex.search(row['paragraph'])
                if match is None:
                    continue
                match_len = len(match.group())
                if match_len > biggest_match_len:
                    biggest_match_len = match_len
                    match_idx = i

            if match_idx is not None:
                rows[match_idx]['paragraph'], n = regex.subn(
                    link, rows[match_idx]['paragraph'], count=1
                )
                self.links_replaced += n
        return rows
