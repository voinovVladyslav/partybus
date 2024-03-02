from .rules import PageType, get_page_type
from .base import BasePageWriter
from .partybus import PartyBusPageWriter


def get_writer(document, data: dict, page_number: int) -> BasePageWriter:
    page_type = get_page_type(page_number)

    if page_type == PageType.PARTY_BUS:
        return PartyBusPageWriter(document, data)

    raise ValueError(f'Unknown page type {page_type}')
