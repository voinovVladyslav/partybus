from .base import BasePageWriter


class PricingPageWriter(BasePageWriter):
    def write(self) -> None:
        self.write_title(self.data['name'])
        for i, row in enumerate(self.data['rows'], 1):
            if i == 1:
                self.write_heading(row['heading'], 1)
            if 2 <= i <= 8:
                self.write_heading(row['heading'], 2)
            else:
                self.write_heading(row['heading'], 3)
            self.write_paragraph(row['paragraph'], make_phone_bold=True)
        self.add_page_break()
