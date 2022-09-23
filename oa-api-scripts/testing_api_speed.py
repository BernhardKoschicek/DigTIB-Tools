import time

import requests

base_url = 'https://openatlas.sarfstation.de/api/0.3/type_entities_all/73?format=geojson&show=types'
#base_url = 'https://connec.openatlas.eu/api/0.3/query/?view_classes=actor&show=types&show=relations&relation_type=P11'
#base_url = 'https://openatlas.sarfstation.de/api/0.3/view_class/actor?format=geojson&show=types'



limit_100 = '&limit=100'
limit_0 = '&limit=0'
start_time = time.time()
initial_data = requests.get(f'{base_url}{limit_100}').json()

pages = list(range(initial_data['pagination']['totalPages']))

results = []
results.extend(initial_data['results'])



for page in pages[1:]:
    data = requests.get(f'{base_url}{limit_100}&page={page + 1}').json()
    results.extend(data['results'])


print("--- %s seconds ---" % (time.time() - start_time))


start_time = time.time()
data_ = requests.get(f'{base_url}{limit_0}').json()
print(len(data_['results']))
print("--- %s seconds ---" % (time.time() - start_time))
