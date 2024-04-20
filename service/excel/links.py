from .utils import transpose, sort_by_wordcount


def aggregate_links(data: list[list]) -> list[dict]:
    data = transpose(data)
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
