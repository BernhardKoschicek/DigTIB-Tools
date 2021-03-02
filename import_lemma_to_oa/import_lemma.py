import json
import numpy
import psycopg2
from bs4 import BeautifulSoup

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
    print(collection)


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
                                 'description': cols[2].text.strip(),
                                 'pages': page[0].text.strip(),
                                 'volume': cols[3].text.strip()})
    return data


def insert_entity(title, code, system_type, date):
    sql = """
        INSERT INTO model.entity (name, system_type, description, begin_from, end_from, class_code)
        VALUES (%(name)s, %(system_type)s, %(description)s, %(begin_from)s, %(end_from)s, %(code)s)
        RETURNING id;"""
    params = {'name': str(title).strip(),
              'system_type': system_type,
              'description': '',
              'begin_from': datetime64_to_timestamp(date),
              'end_from': datetime64_to_timestamp(date),
              'code': code}
    cursor.execute(sql, params)
    return cursor.fetchone()[0]


def insert_link(domain_id, range_id, property_code):
    sql = """
            INSERT INTO model.link (property_code, domain_id, range_id)
            VALUES (
                %(property_code)s, %(domain_id)s, %(range_id)s)
            RETURNING id;"""
    cursor.execute(sql, {'property_code': property_code,
                         'domain_id': domain_id,
                         'range_id': range_id})
    return cursor.fetchone()[0]


lemma_import()
