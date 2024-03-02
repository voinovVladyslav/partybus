from .rules import PageType, get_page_type
from .base import BasePageWriter
from .partybus import PartyBusPageWriter
from .charterbus import CharterBusPageWriter
from .busfleet import BusFleetPageWriter
from .bus import BusPageWriter
from .locations import LocationPageWriter


def get_writer(document, data: dict, page_number: int) -> BasePageWriter:
    page_type = get_page_type(page_number)

    if page_type == PageType.PARTY_BUS:
        return PartyBusPageWriter(document, data)
    if page_type == PageType.CHARTER_BUT:
        return CharterBusPageWriter(document, data)
    if page_type == PageType.BUS_FLEET:
        return BusFleetPageWriter(document, data)
    if page_type == PageType.BUS:
        return BusPageWriter(document, data)
    if page_type == PageType.LOCATIONS:
        return LocationPageWriter(document, data)

    raise ValueError(f'Unknown page type {page_type}')