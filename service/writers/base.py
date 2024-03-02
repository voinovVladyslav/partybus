import re
from abc import ABC, abstractmethod

from docx.shared import RGBColor

from service.banwords import is_banword

RED = RGBColor(255, 0, 0)


class BasePageWriter(ABC):
    def __init__(
        self,
        document,
        data: dict,
        banwords: list[str] = None,
        phone: str = None,
    ):
        self.banwords = banwords or []
        self.phone = phone
        self.document = document
        self.data = data

    def write_title(self, title: str) -> None:
        self.document.add_heading(title, level=0)

    def write_heading(self, heading: str, level: int) -> None:
        text = self._wrap_tag(f'h{level}', heading)
        self.document.add_heading(text, level=level)

    def write_paragraph(
        self, text: str, make_phone_bold: bool = False
    ) -> None:
        if make_phone_bold:
            text = self._make_phone_bold(text)

        paragraph = self.document.add_paragraph('<p>')
        words = text.split()
        for word in words:
            if is_banword(word.lower(), self.banwords):
                run = paragraph.add_run(word + ' ')
                run.font.color.rgb = RED
            elif word.startswith('<strong>') and word.endswith('</strong>'):
                run = paragraph.add_run(word)
                run.bold = True
            else:
                paragraph.add_run(word + ' ')
        self.document.add_paragraph('</p>')

    def _make_phone_bold(self, text: str) -> str:
        if not self.phone:
            return text
        pattern = re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')
        text, _ = pattern.subn(f'<strong>{self.phone}</strong>', text)
        return text

    def _wrap_tag(self, tag: str, text: str) -> str:
        return f'<{tag}>{text}</{tag}>'

    def add_page_break(self) -> None:
        self.document.add_page_break()

    @abstractmethod
    def write(self) -> None:
        raise NotImplementedError('You must implement write method')
