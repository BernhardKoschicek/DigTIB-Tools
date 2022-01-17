import json
import requests


# def start():
#     dedications = requests.get('http://127.0.0.1:5000/api/0.2/node_overview/').json()
#     out = []
#     for dedication in dedications['types'][0]['custom']['Dedication']:
#         print(out)
#         out.append(get_dedication_recursive(dedication, {}))
#     print(out)
#     with open('dedications.json', 'w') as f:
#         json.dump(out, f)
#
#
#
# def get_dedication_recursive(dedication, data):
#     nodes = requests.get(
#         'http://127.0.0.1:5000/api/0.2/node_entities/' + str(dedication['id'])).json()
#     data.update({dedication['label']: {
#         'count': len(nodes['nodes']),
#         'entities': [requests.get(node['url'] + '?show=geometry').json() for node in
#                      nodes['nodes']]}})
#     if dedication['children']:
#         for d in dedication['children']:
#             get_dedication_recursive(d, data)
#     return data


def start():
    dedications = requests.get('http://127.0.0.1:5000/api/0.2/node_entities_all/117731').json()
    out = {
        "type": "FeatureCollection",
        "features": [get_dedications(node) for node in dedications['nodes']]
    }
    with open('dedications.json', 'w') as f:
        json.dump(out, f)

def get_dedications(node):
    entity = requests.get(node['url']).json()
    ded = ''
    for i in entity['features'][0]['types']:
        if 'Dedication' in i['hierarchy']:
            ded = i['label']
    dict = {
        'type': 'Feature',
        'properties': {
            'name': entity['features'][0]['properties']['title'],
            'dedication': ded
        },
        'geometry': get_one_geometry(entity['features'][0]['geometry'])
    }
    return dict

def get_one_geometry(geom):
    if 'GeometryCollection' not in geom['type']:
        return geom
    try:
        print(geom['geometries'][0])
    except:
        return geom
    if geom['geometries'][0]:
        print(geom['geometries'][0])
        return geom['geometries'][0]





start()
