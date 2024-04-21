import enum


class LinkerPageType(str, enum.Enum):
    HOME = "home"
    PARTY_BUS = "party-bus"
    CITY_PAGE = "city-page"
    BUS_FLEET = "bus-fleet"
    CHARTER_BUS = "charter-bus"
    PARTY_BUS_2 = "party-bus-2"
    LOCATIONS = "our-locations"
    MAIN_SERVICE = "main-services"
    WEDDING = "wedding"
    CORPORATE = "corporate"
    AIRPORT = "airport"
    SPORTS_TEAM = "sports-team"
    FIELD_TRIP = "field-trip"
    PRICING = "pricing"
    ABOUT = "about"
    BLOG = "blog"  # do not insert links in this page


HOME_PAGES = [1]
PARTY_BUS_PAGES = range(2, 14)
CITY_PAGES = range(14, 27)
BUS_FLEET_PAGES = [27]
CHARTER_BUS_PAGES = range(28, 33)
PARTY_BUS_PAGES_2 = range(33, 45)
OUR_LOCATIONS_PAGES = [45]
MAIN_SERVICES = [46]
SERVICE_PAGES = range(47, 52)
PRICING_PAGES = [52]
ABOUT_PAGES = [53]
BLOG_PAGES = [54]


def get_linker_page_type(page_number: int) -> LinkerPageType:
    if page_number in HOME_PAGES:
        return LinkerPageType.HOME
    if page_number in PARTY_BUS_PAGES:
        return LinkerPageType.PARTY_BUS
    if page_number in CITY_PAGES:
        return LinkerPageType.CITY_PAGE
    if page_number in BUS_FLEET_PAGES:
        return LinkerPageType.BUS_FLEET
    if page_number in CHARTER_BUS_PAGES:
        return LinkerPageType.CHARTER_BUS
    if page_number in PARTY_BUS_PAGES_2:
        return LinkerPageType.PARTY_BUS_2
    if page_number in OUR_LOCATIONS_PAGES:
        return LinkerPageType.LOCATIONS
    if page_number in MAIN_SERVICES:
        return LinkerPageType.MAIN_SERVICE
    if page_number in PRICING_PAGES:
        return LinkerPageType.PRICING
    if page_number in ABOUT_PAGES:
        return LinkerPageType.ABOUT
    if page_number in BLOG_PAGES:
        return LinkerPageType.BLOG
    raise ValueError(f'Unknown page number {page_number}')
