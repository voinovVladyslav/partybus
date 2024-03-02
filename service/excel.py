from pathlib import Path

import pandas as pd


def read_excel(file_path: Path):
    df = pd.read_excel(
        file_path,
        header=None,
    )
    df.fillna('', inplace=True)
    return df.values.tolist()


def aggregate_data(data: list[list]) -> dict:
    phone = data[0][1]
    is_page_active = False
    result = []
    page_data = {}
    for row in data:
        is_start = bool(row[0] and row[1] and row[3])
        is_end = not bool(row[0] or row[1] or row[3])
        if is_page_active:
            page_data['rows'].append({'heading': row[1], 'paragraph': row[3]})

        if is_start:
            is_page_active = True
            page_data['name'] = row[0]
            page_data['rows'] = []
            page_data['rows'].append({'heading': row[1], 'paragraph': row[3]})

        if is_end:
            is_page_active = False
            if page_data:
                result.append(page_data)
            page_data = {}


    return {
        'phone': phone,
        'pages': result
    }
