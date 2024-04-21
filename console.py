from pathlib import Path

from docx import Document

from service.excel import (
    read_excel, aggregate_data, aggregate_links, get_city_names
)
from service.banwords import load_banwords
from service.writers.factory import get_writer
from service.links.factory import get_linker


filename = 'richmond'
excel_data = read_excel(Path(f'examples/{filename}.xlsx'))
data = aggregate_data(excel_data)

city_names = get_city_names(excel_data)
print(f'Loaded {len(city_names)} city names')

banwords = load_banwords(Path('banwords.txt'))
print(f'Loaded {len(banwords)} banwords')

raw_links = read_excel(Path('examples/links.xlsx'), sheet_name=1)
links = aggregate_links(raw_links, city_names)

document = Document()
for i, page_data in enumerate(data['pages'], 1):
    page_data['name'] = f'{i}. {page_data["name"]}'
    linker = get_linker(i, patterns=links)
    kwargs = {
        'document': document,
        'data': page_data,
        'banwords': banwords,
        'phone': data['phone'],
        'linker': linker,
    }
    writer = get_writer(i, **kwargs)
    print(f'Writing page {i} using {writer.__class__.__name__}...')
    writer.write()

print('Saving document...')
document.save(f'result/{filename}.docx')
print('Done!')
