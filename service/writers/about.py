from .base import BasePageWriter


class AboutPageWriter(BasePageWriter):
    def prepare_data(self) -> None:
        if self.linker is None:
            return
        rows = self.data['rows']
        start, end = rows[:1], rows[1:]
        end = self.linker.render(end)

        if self.linker.links_replaced == 0:
            start = self.linker.render(start)

        self.data['rows'] = start + end

    def write(self) -> None:
        self.write_title(self.data['name'])
        for i, row in enumerate(self.data['rows'], 1):
            if i == 1:
                self.write_heading(row['heading'], 1)
            else:
                self.write_heading(row['heading'], 2)
            self.write_paragraph(row['paragraph'])
        self.add_page_break()
