from .base import BasePageWriter


class CharterBusPageWriter(BasePageWriter):
    def write(self) -> None:
        self.write_title(self.data['name'])
        for i, row in enumerate(self.data['rows'], 1):
            if i == 1:
                self.write_heading(row['heading'], 1)
            if 2 <= i <= 13:
                self.write_heading(row['heading'], 2)
            make_phone_bold = i <= 12
            insert_links = i < 13
            self.write_paragraph(
                row['paragraph'],
                make_phone_bold=make_phone_bold,
                insert_links=insert_links
            )
        self.add_page_break()
