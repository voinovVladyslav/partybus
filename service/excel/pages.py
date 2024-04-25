import re

from service.excel.utils import get_city_names


def aggregate_data(data: list[list]) -> dict:
    pattern = re.compile(r'here is a\b.*?[.,:;]', re.IGNORECASE)
    phone = data[0][1]
    company_name = data[2][1]
    is_page_active = False
    result = []
    page_data = {}
    prev_row = []

    for row in data:
        is_start = bool(row[0] and row[1] and row[3])
        is_end = not bool(row[0] or row[1] or row[3])
        paragraph = row[3]
        paragraph = pattern.sub('', paragraph)

        if is_page_active:
            page_data['rows'].append({
                'heading': row[1], 'paragraph': paragraph
            })

        if is_start:
            if prev_row:
                page_data['city_name'] = prev_row[0]

            is_page_active = True
            page_data['name'] = row[0]
            page_data['rows'] = []
            page_data['rows'].append({
                'heading': row[1], 'paragraph': paragraph
            })

        if is_end:
            is_page_active = False
            if page_data and page_data['rows'] and page_data['name']:
                result.append(page_data)
            page_data = {}
        prev_row = row

    return {
        'company_name': company_name,
        'cities': get_city_names(data),
        'phone': phone,
        'pages': result,
    }
