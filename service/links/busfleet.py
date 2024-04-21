from .base import Linker


class BusFleetLinker(Linker):
    def filter_patterns(self) -> None:
        only = [
            'city_party_bus',
            'pricing',
            'services',
            'airport',
            'field trip',
            'wedding',
            'corporate',
            'sports',
            'home_page',
        ]
        self.patterns = [
            pattern for pattern in self.patterns
            if pattern['header'] in only
        ]
