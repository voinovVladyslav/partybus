import re
from .utils import transpose, sort_by_wordcount


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


def aggregate_links(data: list[list], cities: list[str]) -> list[dict]:
    if not cities:
        cities = []
    data = transpose(data)
    results = []
    for row in data[1:-2]:
        header = row[0].strip().lower().replace(' ', '_')
        link = row[1].strip()
        keywords = sort_by_wordcount([str(x).strip() for x in row[2:] if x])

        if header == 'all_party_bus_pages':
            results.extend(render_buses(header, link, keywords))
            continue

        if header in ['city_party_bus', 'city_charter_bus']:
            results.extend(render_city_links(header, link, keywords, cities))
            continue

        results.append({
            'header': header,
            'link': link,
            'keywords': render_cities(keywords, cities)
        })

    return results


def render_cities(keywords: list[str], cities: list[str]) -> list[str]:
    pattern = re.compile(r'city name|city', flags=re.IGNORECASE)
    processed_keywords = set()

    for city in cities:
        for link in keywords:
            processed_keywords.add(re.sub(pattern, city, link))

    return list(processed_keywords)


def render_buses(header: str, link: str, keywords: list[str]) -> list[dict]:
    result = []
    for bus in BUSES:
        if bus == '30':
            rendered_link = re.sub(r'\/(xx)(.*)\/', r'/30\2-white/', link)
        else:
            rendered_link = re.sub(r'xx', bus, link)
        result.append(
            {
                'header': header,
                'link': rendered_link,
                'keywords': [link.replace('xx', bus) for link in keywords]
            }
        )
    return result


def render_city_links(
    header: str,
    link: str,
    keywords: list[str],
    cities: list[str]
) -> list[dict]:
    pattern = re.compile(r'city', flags=re.IGNORECASE)
    result = []
    for city in cities:
        rendered_link = pattern.sub(city.lower().replace(' ', '-'), link)
        result.append(
            {
                'header': header,
                'link': rendered_link,
                'keywords': sort_by_wordcount(list(set([
                    pattern.sub(city, keyword) for keyword in keywords
                ])))
            }
        )
    return result
