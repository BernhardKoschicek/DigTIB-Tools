import json
from typing import Any

import requests

#
# types = [
#     'Settlement Site agridion selište',
#     'Deserted Village agridion selište',
#     'Existing Village chorion selo',
#     'Rural Settlement',
#     'Estate topos mesto',
#     'Hamlet agridion zaselk',
#     'Village',
#     'Temporary Settlement',
#     'Katun',
#     'Rural Settlement',
#     'Vineyard ampelion vinograd',
#     'Uncultivated Land zabel',
#     'Summer Pasture planena, planina, letovište',
#     'Winter Pasture cheimadion, zimovište',
#     'Meadow pašište livada',
#     'Hunting Grounds lovište zverno',
#     'Fishing Grounds lovište ribno',
#     'Abandoned Land exaleimma eksalimo',
#     'Palace',
#     'Fortification',
#     'Existing Fortification',
#     'Ruined Fortification gradište',
#     'Lower Town',
#     'Fortified Settlement',
#     'Town polis grad',
#     'Metropolis',
#     'Urban Settlement',
#     'Upper Town',
#     'Hamlet agridion zaselk']

url = 'https://openatlas.sarfstation.de/api/0.3/'
endpoint = 'cidoc_class/E18'
parameter = '?format=geojson&limit=9999999'

timezones = [
    ("1282", "1270-01-01", "1283-01-01"),
    ("1300","1283-01-01", "1301-01-01"),
    ("1321","1301-01-01", "1323-01-01"),
    ("1330","1323-01-01", "1331-01-01"),
    ("1334","1330-01-01", "1334-01-01"),
]


def get_types() -> list[str]:
    payload = requests.get(f'{url}type_overview').json()
    d = next((sub for sub in payload['standard'] if sub['name'] == 'Place'), 0)
    return get_types_recursiv(d['children'], [])


def get_types_recursiv(data: list[Any], types: list[Any]) -> list[str]:
    for item in data:
        types.append(item['label'])
    for item in data:
        get_types_recursiv(item['children'], types)
    return types


def get_entities():
    for type_ in get_types():
        for time in timezones:
            search = f'&search={{"beginFrom":[{{"operator":"greaterThanEqual",' \
                     f' "values":["{time[1]}"]}}], ' \
                     f'"endFrom":[{{"operator":"lesserThanEqual",' \
                     f' "values":["{time[2]}"]}}], ' \
                     f' "typeName":[{{"operator":"equal","values":["{type_}"]}}]}}'
            complete_url = f'{url}{endpoint}{parameter}{search}'
            try:
                print(type_)
                data = requests.get(complete_url)
                print(data.json()['results'][0])
                with open(f'{type_} {time[0]}.geojson', 'w') as f:
                    json.dump(data.json()['results'][0], f)
            except:
                print("No values")


get_entities()
