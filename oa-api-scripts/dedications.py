import json
from typing import Any

import requests


def start():
    dedications = requests.get('https://tibopenatlas.orthodoxes-europa.at/api/0.3/type_entities_all/117731?limit=0&format=geojson-v2').json()
    out = {
        "type": "FeatureCollection",
        "features": [get_dedications(node)
                     for node in dedications['results'][0]['features']]
    }
    with open('dedications.json', 'w') as f:
        json.dump(out, f)


def get_dedications(node: dict[str, Any]) -> dict[str, Any]:
    for type_ in node['properties']['types']:
        if 'Dedication' in type_['typeHierarchy']:
            node['properties']['dedication'] = type_['typeName']
    return node


start()
