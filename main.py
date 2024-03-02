from service.excel import read_excel, aggregate_data


data = read_excel('examples/test-partybusfremont.com.xlsx')
data = aggregate_data(data)
print('phone:', data['phone'])
print('pages:', len(data['pages']))
