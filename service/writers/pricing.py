from .base import BasePageWriter


class PricingPageWriter(BasePageWriter):
    def write(self) -> None:
        self.write_title(self.data['name'])
        for i, row in enumerate(self.data['rows'], 1):
            if i == 1:
                self.write_heading(row['heading'], 1)
            if 2 <= i <= 7:
                self.write_heading(row['heading'], 2)
            else:
                self.write_heading(row['heading'], 3)
            self.write_paragraph(row['paragraph'])
        self.add_page_break()
