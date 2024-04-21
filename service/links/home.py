from .base import Linker


class HomeLinker(Linker):
    def filter_patterns(self) -> None:
        headers = [
            'home_page',
            '18_passenger_minibus',
            '20_passenger_minibus',
            '25_passenger_minibus',
            'field_trip',
            'wedding',
            'corporate',
            'sports',
            'city_charter_bus',
        ]
        self.patterns = [
            pattern for pattern in self.patterns if
            pattern['header'].lower() not in headers
        ]
