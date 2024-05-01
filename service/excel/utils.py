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
