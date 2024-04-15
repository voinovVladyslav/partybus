import json
from pathlib import Path

from service.excel import read_excel, aggregate_links


data = read_excel(Path('examples/links.xlsx'))
links = aggregate_links(data)
with open('examples/parsed_links.json', 'w') as f:
    f.write(json.dumps(links, indent=4))
