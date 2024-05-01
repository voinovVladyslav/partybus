from .base import Linker


class BusFleetLinker(Linker):
    def filter_patterns(self) -> None:
        home_page_city = self.kwargs['home_page_city']
        company_name = self.kwargs['company_name']
        only = [
            'city_party_bus',
            'pricing',
            'services',
            'our-locations',
            'home_page',
        ]
        result = []
        for pattern in self.patterns:
            if pattern['header'] == 'home_page':
                new_keywords = []
                for keyword in pattern['keywords']:
                    if home_page_city in keyword.lower():
                        continue
                    if company_name and company_name in keyword:
                        continue
                    new_keywords.append(keyword)

                pattern['keywords'] = new_keywords
                result.append(pattern)
                continue

            if pattern['header'] in only:
                result.append(pattern)

        self.patterns = result
