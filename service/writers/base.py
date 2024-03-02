from abc import ABC, abstractmethod


class BasePageWriter(ABC):
    def __init__(self, document, data: dict):
        self.document = document
        self.data = data

    def write_heading(self, heading: str, level: int) -> None:
        tag = f'h{level}'
        self.document.add_heading(
            self._wrap_tag(tag, heading),
            level=level,
        )

    def write_paragraph(self, paragraph: str) -> None:
        self.document.add_paragraph(self._wrap_tag('p', paragraph))

    def _wrap_tag(self, tag: str, text: str) -> str:
        return f'<{tag}>{text}</{tag}>'

    @abstractmethod
    def write(self) -> None:
        raise NotImplementedError('You must implement write method')
