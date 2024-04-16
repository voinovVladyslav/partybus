import pytest

from service.links.utils import render_cities


@pytest.mark.parametrize(
    ('raw_links', 'cities', 'expected'),
    [
        (['city name'], ['New York'], ['New York']),
        (['CITY NAME'], ['New York'], ['New York']),
        (['CITY'], ['New York'], ['New York']),
        (['CITY in new location'], ['New York'], ['New York in new location']),
    ],

)
def test_link_rendered_single_city(raw_links, cities, expected):
    assert render_cities(raw_links, cities) == expected


@pytest.mark.parametrize(
    ('raw_links', 'cities', 'expected'),
    [
        (['city name', 'city'], ['New York', 'New York'], ['New York']),
        (
            ['city name', 'city'],
            ['New York', 'Washington'],
            ['New York', 'Washington']
        ),
        (
            ['CITY in new location'],
            ['New York', 'Washington'],
            ['New York in new location', 'Washington in new location']
        ),
    ],

)
def test_link_rendered_multiple_cities(raw_links, cities, expected):
    keywords = render_cities(raw_links, cities)
    for keyword in keywords:
        assert keyword in expected
