from pathlib import Path

import pandas as pd


def read_excel(file_path: Path, **kwargs):
    df = pd.read_excel(
        file_path,
        header=None,
        **kwargs
    )
    df.fillna('', inplace=True)
    return df.values.tolist()


def transpose(data: list[list]) -> list[list]:
    return list(map(list, zip(*data)))


def sort_by_wordcount(data: list[str]) -> list[str]:
    return sorted(data, key=lambda x: len(x.split()), reverse=True)


def get_city_names(data: list[list]) -> set[str]:
    cities = set()
    for row in data[1:]:
        if row[0] and row[1] and not row[2] and not row[3]:
            cities.add(row[0].strip())
    return cities
