from pathlib import Path

from docx import Document

from service.excel import read_excel, aggregate_data, aggregate_links
from service.banwords import load_banwords
from service.writers.factory import get_writer
from service.links.factory import get_linker


filename = 'fortworth'
excel_data = read_excel(Path(f'examples/{filename}.xlsx'))
data = aggregate_data(excel_data)

print(f'Home page city: {data["home_page_city"]}')
print(f'Party bus cities: {data["party_bus_cities"]}')
print(f'Charter bus cities: {data["charter_bus_cities"]}')
print(f'Company name: {data["company_name"]}')

banwords = load_banwords(Path('banwords.txt'))
print(f'Loaded {len(banwords)} banwords')

raw_links = read_excel(Path('examples/links.xlsx'), sheet_name=1)
links = aggregate_links(
    data=raw_links,
    home_page_city=data['home_page_city'],
    party_bus_cities=data['party_bus_cities'],
    charter_bus_cities=data['charter_bus_cities'],
    company_name=data['company_name']
)

document = Document()
for i, page_data in enumerate(data['pages'], 1):
    page_data['name'] = f'{i}. {page_data["name"]}'
    linker = get_linker(
        page_number=i,
        patterns=links,
        home_page_city=data['home_page_city'],
        company_name=data['company_name'],
        city_name=page_data['city_name'],
    )
    kwargs = {
        'document': document,
        'data': page_data,
        'banwords': banwords,
        'phone': data['phone'],
        'linker': linker,
    }
    writer = get_writer(i, **kwargs)
    print(
        f'Writing page {i} using '
        f'{writer.__class__.__name__} '
        f'and {linker.__class__.__name__}...'
    )
    writer.write()
    print('Links replaced:', linker.links_replaced)

print('Saving document...')
document.save(f'result/{filename}.docx')
print('Done!')
