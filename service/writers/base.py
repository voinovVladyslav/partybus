from abc import ABC, abstractmethod


class BasePageWriter(ABC):
    def __init__(self, document, data: dict):
        self.document = document
        self.data = data

    def write_title(self, title: str) -> None:
        self.document.add_heading(title, level=0)

    def write_heading(self, heading: str, level: int) -> None:
        text = self._wrap_tag(f'h{level}', heading)
        self.document.add_heading(text, level=level)

    def write_paragraph(self, paragraph: str) -> None:
        self.document.add_paragraph(self._wrap_tag('p', paragraph))

    def _wrap_tag(self, tag: str, text: str) -> str:
        return f'<{tag}>{text}</{tag}>'

    def add_page_break(self) -> None:
        self.document.add_page_break()

    @abstractmethod
    def write(self) -> None:
        raise NotImplementedError('You must implement write method')
