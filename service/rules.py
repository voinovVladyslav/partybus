import enum


class PageType(enum.Enum, str):
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
