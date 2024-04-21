from .base import BasePageWriter


class LocationPageWriter(BasePageWriter):
    def write(self) -> None:
        self.write_title(self.data['name'])
        for i, row in enumerate(self.data['rows'], 1):
            if i == 1:
                self.write_heading(row['heading'], 1)
            self.write_paragraph(row['paragraph'], insert_links=True)
        self.add_page_break()
