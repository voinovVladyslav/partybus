from .base import Linker


class PartyBus2Linker(Linker):
    def filter_patterns(self) -> None:
        exclude = [
            'our_fleet',
            'all_party_bus_pages',
            '18_passenger_minibus',
            '20_passenger_minibus',
            '25_passenger_minibus',
            '56_passenger_minibus',
            'city_party_bus',
        ]
        self.patterns = [
            pattern for pattern in self.patterns
            if pattern['header'] not in exclude
        ]
