from service.links.base import Linker


def test_linker_single_match():
    patterns = [
        {
            'header': 'Home',
            'link': '/home/',
            'keywords': ['country', 'home']
        }
    ]
    linker = Linker(patterns)
    text = 'This is my country'
    rendered_text = linker.render(text)
    assert rendered_text == 'This is my <a href="/home/">country</a>'


def test_linker_multiple_matches():
    patterns = [
        {
            'header': 'Home',
            'link': '/home/',
            'keywords': ['country', 'home']
        }
    ]
    linker = Linker(patterns)
    text = 'This country is my home'
    rendered_text = linker.render(text)
    assert rendered_text == 'This <a href="/home/">country</a> is my home'


def test_linker_multiple_patterns_multiple_matches():
    patterns = [
        {
            'header': 'Home',
            'link': '/home/',
            'keywords': ['home']
        },
        {
            'header': 'Country',
            'link': '/country/',
            'keywords': ['country']
        }
    ]
    linker = Linker(patterns)
    text = 'This country is my home'
    rendered_text = linker.render(text)
    assert rendered_text == 'This <a href="/country/">country</a> is my <a href="/home/">home</a>'  # noqa


def test_linker_single_match_with_overlaping_keywords():
    patterns = [
        {
            'header': 'Home',
            'link': '/home/',
            'keywords': ['home country', 'home']
        }
    ]
    linker = Linker(patterns)
    text = 'This is my home country.'
    rendered_text = linker.render(text)
    assert rendered_text == 'This is my <a href="/home/">home country</a>.'


def test_linker_match_start_of_string():
    patterns = [
        {
            'header': 'Home',
            'link': '/home/',
            'keywords': ['country', 'home']
        }
    ]
    linker = Linker(patterns)
    text = 'country is sdfs'
    rendered_text = linker.render(text)
    assert rendered_text == '<a href="/home/">country</a> is sdfs'


def test_linker_does_not_render_keywords_in_href():
    patterns = [
        {
            'header': 'Home',
            'link': '/home/',
            'keywords': ['country', 'home']
        }
    ]
    linker = Linker(patterns)
    text = '<a href="/home/">country</a> is sdfs'
    rendered_text = linker.render(text)
    assert rendered_text == '<a href="/home/">country</a> is sdfs'


def test_linker_does_not_insert_link_twice_for_his_lifetime():
    patterns = [
        {
            'header': 'Home',
            'link': '/home/',
            'keywords': ['country', 'home']
        }
    ]
    linker = Linker(patterns)
    text = 'country is home'
    rendered_text = linker.render(text)
    assert rendered_text == '<a href="/home/">country</a> is home'
    rendered_text = linker.render(rendered_text)
    assert rendered_text == '<a href="/home/">country</a> is home'


def test_no_two_links_without_separators():
    patterns = [
        {
            'header': 'Home',
            'link': '/home/',
            'keywords': ['home']
        },
        {
            'header': 'Country',
            'link': '/country/',
            'keywords': ['country']
        },
    ]
    linker = Linker(patterns)
    text = 'home country'
    rendered_text = linker.render(text)
    assert rendered_text == '<a href="/home/">home</a> country'


def test_no_two_links_without_separators_reverse():
    patterns = [
        {
            'header': 'Country',
            'link': '/country/',
            'keywords': ['country']
        },
        {
            'header': 'Home',
            'link': '/home/',
            'keywords': ['home']
        },
    ]
    linker = Linker(patterns)
    text = 'home country'
    rendered_text = linker.render(text)
    assert rendered_text == 'home <a href="/country/">country</a>'
