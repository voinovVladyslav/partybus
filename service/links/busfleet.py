from .base import Linker


class BusFleetLinker(Linker):
    def filter_patterns(self) -> None:
        only = [
            'city_party_bus',
            'pricing',
            'services',
            'our-locations',
            'home_page',
        ]
        self.patterns = [
            pattern for pattern in self.patterns
            if pattern['header'] in only
        ]
