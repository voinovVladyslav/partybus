import re


def render_cities(raw_links: list[str], cities: list[str]) -> list[str]:
    pattern = re.compile(r'city name|city', flags=re.IGNORECASE)
    processed_links = set()

    for city in cities:
        for link in raw_links:
            processed_links.add(re.sub(pattern, city, link))

    return list(processed_links)
