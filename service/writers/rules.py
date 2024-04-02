import enum


class PageType(str, enum.Enum):
    HOME_PAGE = "home"
    BUS = "bus"
    LOCATIONS = "our-locations"
    MAIN_SERVICE = "main-services"
    SERVICE = "service"
    PRICING = "pricing"
    ABOUT = "about"
    BLOG = "blog"


HOME_PAGE = [1]
BUS_PAGES = range(2, 8)
OUR_LOCATIONS_PAGES = [8]
MAIN_SERVICES = [9]
SERVICE_PAGES = range(10, 15)
PRICING_PAGES = [15]
ABOUT_PAGES = [16]
BLOG_PAGE = [17]


def get_page_type(page_number: int) -> PageType:
    if page_number in HOME_PAGE:
        return PageType.HOME_PAGE
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
