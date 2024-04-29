from .base import BasePageWriter


class CharterBusPageWriter(BasePageWriter):
    def prepare_data(self) -> None:
        if self.linker is None:
            return
        rows = self.data['rows']
        start, end = rows[:11], rows[11:]
        start = self.linker.render(start)
        self.data['rows'] = start + end

    def write(self) -> None:
        self.write_title(self.data['name'])
        for i, row in enumerate(self.data['rows'], 1):
            if i == 1:
                self.write_heading(row['heading'], 1)
            if 2 <= i <= 13:
                self.write_heading(row['heading'], 2)
            make_phone_bold = i <= 12
            self.write_paragraph(
                row['paragraph'],
                make_phone_bold=make_phone_bold,
            )
        self.add_page_break()
