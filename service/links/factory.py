from .rules import LinkerPageType, get_linker_page_type

from .base import Linker
from .home import HomeLinker


def get_linker(page_number: int, **kwargs) -> Linker:
    page_type = get_linker_page_type(page_number)

    if page_type == LinkerPageType.HOME:
        return HomeLinker(**kwargs)

    raise ValueError(f'Unknown page type {page_type}')

