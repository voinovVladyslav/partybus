from .base import BasePageWriter


class BusFleetPageWriter(BasePageWriter):
    def write(self) -> None:
        self.write_title(self.data['name'])
        for i, row in enumerate(self.data['rows'], 1):
            if i == 1:
                self.write_heading(row['heading'], 1)
            else:
                self.write_heading(row['heading'], 2)
            self.write_paragraph(row['paragraph'])
        self.add_page_break()
