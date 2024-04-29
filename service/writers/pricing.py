from .base import BasePageWriter


class PricingPageWriter(BasePageWriter):
    def prepare_data(self) -> None:
        if self.linker is None:
            return
        rows = self.data['rows']
        start, middle, end = rows[:1], rows[1:8], rows[8:]
        middle = self.linker.render(middle)

        if self.linker.links_replaced == 0:
            start = self.linker.render(start)

        self.data['rows'] = start + middle + end

    def write(self) -> None:
        self.write_title(self.data['name'])
        for i, row in enumerate(self.data['rows'], 1):
            if i == 1:
                self.write_heading(row['heading'], 1)
            if 2 <= i <= 8:
                self.write_heading(row['heading'], 2)
            else:
                self.write_heading(row['heading'], 3)
            self.write_paragraph(row['paragraph'])
        self.add_page_break()
