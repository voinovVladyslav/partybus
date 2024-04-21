import re


BUSES = [
    '14',
    '15',
    '18',
    '20',
    '22',
    '25',
    '30',
    '35',
    '36',
    '40',
    '50',
]


def render_cities(raw_links: list[str], cities: list[str]) -> list[str]:
    pattern = re.compile(r'city name|city', flags=re.IGNORECASE)
    processed_links = set()

    for city in cities:
        for link in raw_links:
            processed_links.add(re.sub(pattern, city, link))

    return list(processed_links)


def render_buses(raw_links: list[str]) -> list[str]:
    pattern = re.compile(r'xx', flags=re.IGNORECASE)
    processed_links = set()

    for bus in BUSES:
        for link in raw_links:
            processed_links.add(re.sub(pattern, bus, link))

    return list(processed_links)
