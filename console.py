import json

from docx import Document
from pathlib import Path

from service.excel import read_excel, aggregate_data
from service.banwords import load_banwords
from service.writers.factory import get_writer


site_name = 'fort_test'


data = read_excel(Path(f'examples/{site_name}.xlsx'))
data = aggregate_data(data)

banwords = load_banwords(Path('banwords.txt'))
print(f'Loaded {len(banwords)} banwords')

with open(f'examples/{site_name}.json', 'w') as f:
    json.dump(data, f, indent=4)

document = Document()
for i, page_data in enumerate(data['pages'][1:], 1):
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
document.save(f'result/{site_name}.docx')
print('Done!')
