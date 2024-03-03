from docx import Document

from service.excel import read_excel, aggregate_data
from service.banwords import load_banwords
from service.writers.factory import get_writer


data = read_excel('examples/partybusesarlington.xlsx')
data = aggregate_data(data)

banwords = load_banwords('banwords.txt')
print(f'Loaded {len(banwords)} banwords')

document = Document()
for i, page_data in enumerate(data['pages'], 1):
    page_data['name'] = f'{i}. {page_data["name"]}'
    kwargs = {
        'document': document,
        'data': page_data,
        'banwords': banwords,
        'phone': data['phone'],
    }
    writer = get_writer(i, **kwargs)
    print(f'Writing page {i} using {writer.__class__.__name__}...')
    writer.write()

print('Saving document...')
document.save('result/partybusesarlington.docx')
print('Done!')
