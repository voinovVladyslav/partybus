from .rules import LinkerPageType, get_linker_page_type

from .base import Linker
from .home import HomeLinker
from .partybus import PartyBusLinker
from .city import CityLinker


def get_linker(page_number: int, **kwargs) -> Linker:
    page_type = get_linker_page_type(page_number)

    if page_type == LinkerPageType.HOME:
        return HomeLinker(**kwargs)
    if page_type == LinkerPageType.PARTY_BUS:
        return PartyBusLinker(**kwargs)
    if page_type == LinkerPageType.CITY_PAGE:
        return CityLinker(**kwargs)

    raise ValueError(f'Unknown page type {page_type}')
