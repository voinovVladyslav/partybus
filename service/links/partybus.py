from .base import Linker


class PartyBusLinker(Linker):
    def filter_patterns(self) -> None:
        exclude = [
            'city_charter_bus',
        ]
        headers = [
            '18_passenger_minibus',
            '20_passenger_minibus',
            '25_passenger_minibus',
            '56_passenger_charter_bus',
        ]

        rules = []
        patterns = [
            '{}-passenger',
            '{} passenger',
            '{}-passengers',
            '{} passengers',
            '{}',
        ]
        for pattern in patterns:
            rules += [pattern.format(i) for i in [18, 20, 25, 56]]

        for pattern in self.patterns:
            if pattern['header'] not in headers:
                continue
            pattern['keywords'] = [
                word for word in pattern['keywords']
                if word not in rules
            ]
        self.patterns = [
            pattern for pattern in self.patterns
            if pattern['header'] not in exclude
        ]
