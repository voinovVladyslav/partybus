import json
from pathlib import Path


def transpose(data: list[list]) -> list[list]:
    return list(map(list, zip(*data)))


def sort_by_wordcount(data: list[str]) -> list[str]:
    return sorted(data, key=lambda x: len(x.split()), reverse=True)


def get_city_names():
    pass


def aggregate_links():
    data = json.loads(Path('examples/links_transposed.json').read_text())
    

    results = []
    for row in data[1:-2]:
        header = row[0].strip().lower().replace(' ', '_')
        link = row[1].strip()
        links = sort_by_wordcount([str(x).strip() for x in row[2:] if x])
        results.append({
            'header': header,
            'link': link,
            'keywords': links
        })

    return results

links = aggregate_links()
with open('examples/parsed_links.json', 'w') as f:
    f.write(json.dumps(links, indent=4))
