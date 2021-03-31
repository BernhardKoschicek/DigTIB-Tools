import json
import numpy
import psycopg2
from bs4 import BeautifulSoup
import re

conn = psycopg2.connect(
    host="localhost",
    database="openatlas",
    user="openatlas",
    password="openatlas")

cursor = conn.cursor()


def lemma_import():
    # source_list = ['lists/tib1_lemma.txt', 'lists/tib2_output.txt', 'lists/tib3_output.txt',
    #                'lists/tib4_output.txt', 'lists/tib5_output.txt', 'lists/tib6_output.txt',
    #                'lists/tib7_output.txt', 'lists/tib8_output.txt', 'lists/tib9_output.txt',
    #                'lists/tib10_output.txt', 'lists/tib12_output.txt', 'lists/tib13_output.txt']
    source_list = ['lists/tib1_lemma.txt', 'lists/tib3_output.txt', 'lists/tib6_output.txt',
                   'lists/tib12_output.txt']
    collection = get_data(source_list)
    tib_volumes = {"TIB1": {"book_id": "124482", "external_id": "124476", "case_id": "124484"},
                   "TIB3": {"book_id": "124489", "external_id": "124477", "case_id": "124485"},
                   "TIB6": {"book_id": "124490", "external_id": "124478", "case_id": "124486"},
                   "TIB12": {"book_id": "124491", "external_id": "124493", "case_id": "124487"}}

    for i in collection:
        lemma = {**i, **tib_volumes[i["volume"]]}
        place_id = insert_entity(name=lemma['name'], code='E18', system_type='place',
                                 description=lemma['notes'])

        # Link to Location
        location_id = insert_entity(name='Location of ' + lemma['name'], code='E53',
                                    system_type='place location', description=None)
        insert_link(domain_id=place_id, range_id=location_id, property_code='P53', description=None,
                    type_id=None)

        # Link to Case Study
        insert_link(domain_id=place_id, range_id=lemma['case_id'], property_code='P2',
                    description=None,
                    type_id=None)

        # Link to Ext Ref
        page = None
        if re.findall(r'^(.*?)\D+', lemma['pages']):
            page = re.findall(r'^(.*?)\D+', lemma['pages'])[0]
        if not page:
            page = lemma['pages']
        insert_link(domain_id=lemma['external_id'], range_id=place_id, property_code='P67',
                    description=page, type_id="117448")

        # Link to Reference
        insert_link(domain_id=lemma['book_id'], range_id=place_id, property_code='P67',
                    description=lemma['pages'], type_id=None)

        conn.commit()


def get_data(source_list):
    data = []
    for source in source_list:
        print(source)
        with open(source, encoding="utf8") as f:
            for row in BeautifulSoup(f, "html.parser")("tr"):
                if row.find_all("b"):
                    cols = row.find_all('td')
                    page = cols[1].find_all('b')
                    data.append({'name': cols[0].text.strip(),
                                 'notes': cols[2].text.strip(),
                                 'pages': page[0].text.strip(),
                                 'volume': cols[3].text.strip().replace(" ", "")})
    return data


def insert_entity(name, code, system_type, description):
    sql = """
        INSERT INTO model.entity (name, system_type, description, class_code)
        VALUES (%(name)s, %(system_type)s, %(description)s, %(code)s)
        RETURNING id;"""
    params = {'name': str(name).strip(),
              'system_type': system_type,
              'description': description,
              'code': code}
    cursor.execute(sql, params)
    return cursor.fetchone()[0]


def insert_link(domain_id, range_id, property_code, description, type_id):
    sql = """
            INSERT INTO model.link (property_code, domain_id, range_id, description, type_id)
            VALUES (
                %(property_code)s, %(domain_id)s, %(range_id)s, %(description)s, %(type_id)s)
            RETURNING id;"""
    cursor.execute(sql, {'property_code': property_code,
                         'domain_id': domain_id,
                         'range_id': range_id,
                         'description': description,
                         'type_id': type_id})
    return cursor.fetchone()[0]


lemma_import()
