from abc import ABC, abstractmethod

from docx.shared import RGBColor

from service.banwords import is_banword

RED = RGBColor(255, 0, 0)


class BasePageWriter(ABC):
    def __init__(self, document, data: dict, banwords: list[str] = None):
        self.banwords = banwords or []
        self.document = document
        self.data = data

    def write_title(self, title: str) -> None:
        self.document.add_heading(title, level=0)

    def write_heading(self, heading: str, level: int) -> None:
        text = self._wrap_tag(f'h{level}', heading)
        self.document.add_heading(text, level=level)

    def write_paragraph(self, text: str) -> None:
        paragraph = self.document.add_paragraph('<p>')
        words = text.split()
        for word in words:
            if is_banword(word.lower(), self.banwords):
                run = paragraph.add_run(word + ' ')
                run.font.color.rgb = RED
            else:
                paragraph.add_run(word + ' ')
        self.document.add_paragraph('</p>')

    def _wrap_tag(self, tag: str, text: str) -> str:
        return f'<{tag}>{text}</{tag}>'

    def add_page_break(self) -> None:
        self.document.add_page_break()

    @abstractmethod
    def write(self) -> None:
        raise NotImplementedError('You must implement write method')
