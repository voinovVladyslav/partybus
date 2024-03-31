import pytest

from service.phones import strong_phones


@pytest.mark.parametrize(
    ('text', 'phone', 'expected'),
    [
        (
            'Call me at 123-456-7890',
            '123-456-7890',
            'Call me at <strong>123-456-7890</strong>',
        ),
        (
            'Call me at 123-456-7890.',
            '123-456-7890',
            'Call me at <strong>123-456-7890</strong>.'
        ),
        (
            'Call me at 123-456-7890 or 123-456-7890',
            '123-456-7890',
            (
                'Call me at <strong>123-456-7890</strong> '
                'or <strong>123-456-7890</strong>'
            )
        ),
        (
            'Call me at (123) 456 7890 or 333 456 7890',
            '123-456-7890',
            (
                'Call me at <strong>123-456-7890</strong> '
                'or <strong>123-456-7890</strong>'
            )
        ),
        (
            '38103 (901) 526-0110 <h3>',
            '123-456-7890',
            '38103 <strong>123-456-7890</strong> <h3>'
        ),
    ],

)
def test_strong_phones(text, phone, expected):
    assert strong_phones(text, phone) == expected
