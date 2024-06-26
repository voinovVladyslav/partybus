from .rules import PageType, get_page_type
from .base import BasePageWriter
from .bus import BusPageWriter
from .locations import LocationPageWriter
from .mainservice import MainServicePageWriter
from .service import ServicePageWriter
from .pricing import PricingPageWriter
from .about import AboutPageWriter
from .blog import BlogPageWriter
from .home import HomePageWriter


def get_writer(page_number: int, **kwargs) -> BasePageWriter:
    page_type = get_page_type(page_number)

    if page_type == PageType.HOME_PAGE:
        return HomePageWriter(**kwargs)
    if page_type == PageType.BUS:
        return BusPageWriter(**kwargs)
    if page_type == PageType.LOCATIONS:
        return LocationPageWriter(**kwargs)
    if page_type == PageType.MAIN_SERVICE:
        return MainServicePageWriter(**kwargs)
    if page_type == PageType.SERVICE:
        return ServicePageWriter(**kwargs)
    if page_type == PageType.PRICING:
        return PricingPageWriter(**kwargs)
    if page_type == PageType.ABOUT:
        return AboutPageWriter(**kwargs)
    if page_type == PageType.BLOG:
        return BlogPageWriter(**kwargs)

    raise ValueError(f'Unknown page type {page_type}')
