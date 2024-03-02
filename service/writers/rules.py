import enum


class PageType(str, enum.Enum):
    PARTY_BUS = "party-bus"
    CHARTER_BUT = "charter-bus"
    BUS_FLEET = "bus-fleet"
    BUS = "bus"
    LOCATIONS = "our-locations"
    MAIN_SERVICE = "main-services"
    SERVICE = "service"
    PRICING = "pricing"
    ABOUT = "about"
    BLOG = "blog"


PARTY_BUS_PAGES = range(1, 14)
CHARTER_BUS_PAGES = range(14, 27)
BUS_FLEET_PAGES = [27]
BUS_PAGES = range(27, 45)
OUR_LOCATIONS_PAGES = [45]
MAIN_SERVICES = [46]
SERVICE_PAGES = range(46, 52)
PRICING_PAGES = [52]
ABOUT_PAGES = [53]
BLOG_PAGE = [54]


def get_page_type(page_number: int) -> PageType:
    if page_number in PARTY_BUS_PAGES:
        return PageType.PARTY_BUS
    if page_number in CHARTER_BUS_PAGES:
        return PageType.CHARTER_BUT
    if page_number in BUS_FLEET_PAGES:
        return PageType.BUS_FLEET
    if page_number in BUS_PAGES:
        return PageType.BUS
    if page_number in OUR_LOCATIONS_PAGES:
        return PageType.LOCATIONS
    if page_number in MAIN_SERVICES:
        return PageType.MAIN_SERVICE
    if page_number in SERVICE_PAGES:
        return PageType.SERVICE
    if page_number in PRICING_PAGES:
        return PageType.PRICING
    if page_number in ABOUT_PAGES:
        return PageType.ABOUT
    if page_number in BLOG_PAGE:
        return PageType.BLOG
    raise ValueError(f'Unknown page number {page_number}')
