from .base import BasePageWriter


class PartyBusPageWriter(BasePageWriter):
    def write(self) -> None:
        self.write_heading(self.data['name'], 0)
        for i, row in enumerate(self.data['rows'], 1):
            if i == 1:
                self.write_heading(row['heading'], 1)
            if 2 <= i <= 9:
                self.write_heading(row['heading'], 2)
            self.write_paragraph(row['paragraph'])
