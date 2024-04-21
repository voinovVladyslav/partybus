from .rules import LinkerPageType, get_linker_page_type

from .base import Linker
from .home import HomeLinker
from .partybus import PartyBusLinker
from .city import CityLinker
from .busfleet import BusFleetLinker
from .charterbus import CharterBusLinker
from .partybus2 import PartyBus2Linker
from .locations import LocationsLinker


def get_linker(page_number: int, **kwargs) -> Linker:
    page_type = get_linker_page_type(page_number)

    if page_type == LinkerPageType.HOME:
        return HomeLinker(**kwargs)
    if page_type == LinkerPageType.PARTY_BUS:
        return PartyBusLinker(**kwargs)
    if page_type == LinkerPageType.CITY_PAGE:
        return CityLinker(**kwargs)
    if page_type == LinkerPageType.BUS_FLEET:
        return BusFleetLinker(**kwargs)
    if page_type == LinkerPageType.CHARTER_BUS:
        return CharterBusLinker(**kwargs)
    if page_type == LinkerPageType.PARTY_BUS_2:
        return PartyBus2Linker(**kwargs)
    if page_type == LinkerPageType.LOCATIONS:
        return LocationsLinker(**kwargs)

    raise ValueError(f'Unknown page type {page_type}')
