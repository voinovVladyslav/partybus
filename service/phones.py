import re


def strong_phones(text: str, phone: str) -> str:
    pattern = re.compile(r'\(?\d{3}.{0,3}?\d{3}.{0,2}\d{4}')
    text = pattern.sub(f'<strong>{phone}</strong>', text)
    return text
