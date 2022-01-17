import json
import requests

entities = ['Arbanasi',
            'Běla Crьkva',
            'Běla Vodica',
            'Bistrica',
            'Bogomilja',
            'Bohorino',
            'Bučinь',
            'Dlьga Vьsi',
            'Drěnovьci',
            'Dubnica',
            'Dupijačanje',
            'Dušnikь',
            'Eleněžьci',
            'Galičane',
            'Gostovša',
            'Homorani',
            'Horupanь',
            'Komarьčene',
            'Kostěnьče',
            'Kostino',
            'Krivogaštani',
            'Kučьkověne',
            'Lepьče',
            'Margaritь',
            'Mogilěni',
            'Mramorane',
            'Nebrěgovo',
            'Něgiga',
            'Ōbrьšani',
            'Ōrěhoь dolь',
            'Rakita',
            'Sopotnica',
            'Svetyi Dimitrïe',
            'Tehovo',
            'Trьnovьci',
            'Žurьče',
            ]

wrong = []
for entity in entities:
    try:
        data = requests.get('http://127.0.0.1:5000/api/0.2/class/E18?filter=and|name|eq|' + entity)

        print(data.json())
    except:
        wrong.append(entity)
        continue

print(wrong)
