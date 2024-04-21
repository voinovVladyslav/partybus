import re

from .base import Linker


class CityLinker(Linker):
    def filter_patterns(self) -> None:
        exclude_patterns = [
            re.compile(r'^\d\d-passenger$'), 
            re.compile(r'^\d\d passenger$'),
            re.compile(r'^\d\d-passengers$'),
            re.compile(r'^\d\d passengers$'),
            re.compile(r'^\d\d$'),
        ]
        for pattern in self.patterns:
            if pattern['header'] != 'all_party_bus_pages':
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
                

