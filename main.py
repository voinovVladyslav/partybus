from docx import Document

from service.excel import read_excel, aggregate_data
from service.writers.factory import get_writer


data = read_excel('examples/test-partybusfremont.com.xlsx')
data = aggregate_data(data)


document = Document()
for i, page_data in enumerate(data['pages'], 1):
    page_data['name'] = f'{i}. {page_data["name"]}'
    writer = get_writer(document, page_data, i)
    writer.write()

document.save('result/partybusfremont.docx')
