import re

from .base import Linker


class AboutLinker(Linker):
    def filter_patterns(self) -> None:
        exclude = [
            'about',
            'city_charter_bus',
        ]
        self.patterns = [
            pattern for pattern in self.patterns
            if pattern['header'] not in exclude
        ]

        exclude_patterns = [
            re.compile(r'^\d\d-passenger$'),
            re.compile(r'^\d\d passenger$'),
            re.compile(r'^\d\d-passengers$'),
            re.compile(r'^\d\d passengers$'),
            re.compile(r'^\d\d$'),
        ]
        partial_filter = [
            '18_passenger_minibus',
            '20_passenger_minibus',
            '25_passenger_minibus',
            '56_passenger_charter_bus',
        ]
        for pattern in self.patterns:
            if pattern['header'] not in partial_filter:
                continue
            keywords = []
            for keyword in pattern['keywords']:
                add = True
                for exclude_pattern in exclude_patterns:
                    if exclude_pattern.match(keyword):
                        add = False
                if add:
                    keywords.append(keyword)

            pattern['keywords'] = keywords
