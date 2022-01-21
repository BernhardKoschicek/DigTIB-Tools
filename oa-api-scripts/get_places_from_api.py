import json
from typing import Any

import requests

base_url = 'https://openatlas.sarfstation.de/api/0.3/'
endpoint = 'cidoc_class/E18'
parameter = '?format=geojson&limit=9999999'

timezones = [
    ("1282", "1270-01-01", "1283-01-01"),
    ("1300", "1283-01-01", "1301-01-01"),
    ("1321", "1301-01-01", "1323-01-01"),
    ("1330", "1323-01-01", "1331-01-01"),
    ("1334", "1330-01-01", "1334-01-01")]


def get_types() -> list[str]:
    payload = requests.get(f'{base_url}type_overview').json()
    d = next((sub for sub in payload['standard'] if sub['name'] == 'Place'), 0)
    return get_types_recursive(d['children'], [])


def get_types_recursive(data: list[Any], types: list[Any]) -> list[str]:
    for item in data:
        types.append(item['label'])
    for item in data:
        get_types_recursive(item['children'], types)
    return types


def get_entities():
    for type_ in get_types():
        for time in timezones:
            search = f'&search={{"beginFrom":[' \
                     f'{{"operator":"greaterThanEqual",' \
                     f'"values":["{time[1]}"]}}],' \
                     f'"endFrom":[{{"operator":"lesserThanEqual",' \
                     f'"values":["{time[2]}"]}}],' \
                     f'"typeName":[{{"operator":"equal",' \
                     f'"values":["{type_}"]}}]}}'
            url = f'{base_url}{endpoint}{parameter}{search}'
            try:
                with open(f'{type_} {time[0]}.geojson', 'w') as f:
                    json.dump(requests.get(url).json()['results'][0], f)
            except Exception as e:
                print(e)


get_entities()
