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
    ],

)
def test_strong_phones(text, phone, expected):
    assert strong_phones(text, phone) == expected
