from docx import Document

from service.excel import read_excel, aggregate_data


data = read_excel('examples/test-partybusfremont.com.xlsx')
data = aggregate_data(data)
print('phone:', data['phone'])
print('pages:', len(data['pages']))

for page in data['pages']:
    pass

document = Document()
document.add_heading('Party Bus Fremont', level=0)
document.add_heading('Heading 1', level=1)
document.add_paragraph('Paragraph 1')
document.add_page_break()
document.add_heading('Party Bus Fremont', level=0)
document.add_heading('Heading 1', level=1)
document.add_paragraph('Paragraph 1')
document.save('result/partybusfremont.docx')
