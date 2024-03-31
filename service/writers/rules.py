import enum


class PageType(str, enum.Enum):
    HOME_PAGE = "home"
    BUS = "bus"
    BUS_FLEET = "bus-fleet"
    LOCATIONS = "our-locations"
    MAIN_SERVICE = "main-services"
    SERVICE = "service"
    PRICING = "pricing"
    ABOUT = "about"
    BLOG = "blog"


HOME_PAGE = [1]
BUS_PAGES = range(2, 8)
BUS_FLEET_PAGES = [8]
OUR_LOCATIONS_PAGES = [9]
MAIN_SERVICES = [10]
SERVICE_PAGES = range(11, 16)
PRICING_PAGES = [16]
ABOUT_PAGES = [17]
BLOG_PAGE = [18]


def get_page_type(page_number: int) -> PageType:
    if page_number in HOME_PAGE:
        return PageType.HOME_PAGE
    if page_number in BUS_PAGES:
        return PageType.BUS
    if page_number in BUS_FLEET_PAGES:
        return PageType.BUS_FLEET
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
