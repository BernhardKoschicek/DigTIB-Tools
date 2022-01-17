import numpy
import psycopg2
import json

conn = psycopg2.connect(
    host="localhost",
    database="openatlas",
    user="openatlas",
    password="openatlas")

cursor = conn.cursor()


def gis_import():
    collection = get_data('source/montenegro_routes.geojson')
    data = []

    for entity in collection:
        location_id = None
        ####### For border lines
        # for i in data:
        #     if entity['name'] in i['name'] and entity['date'] in i['date']:
        #         location_id = i['location_id']
        #         insert_geom(entity_id=location_id, geom=entity['geom'], title=entity['title'])
        # if location_id is None:
        #     location_id = insert_entity(title='Location of ' + entity['title'], code='E53',
        #                             system_type='place location', date=entity['date'])
        # else:
        #     continue

        ####### For border lines
        # place_id = insert_entity(title='Border ' + entity['title'], code='E18', system_type='place',
        #                          date=entity['date'])
        # place_id = insert_entity(title='Old Road ' + entity['title'], code='E18', system_type='place',
        #                          date=None)
        place_id = insert_entity(title=entity['title'], code='E18', system_class='place',
                                 date=None)
        location_id = insert_entity(title='Location of ' + entity['title'], code='E53',
                                    system_class='object_location', date=None)
        insert_link(domain_id=place_id, range_id=location_id, property_code='P53')
        # insert_link(domain_id=place_id, range_id=123338, property_code='P2')  # Link to Place Type
        # insert_link(domain_id=place_id, range_id=116482, property_code='P2')  # Link to Case Study "Macedonian Road System" (TIB)
        # insert_link(domain_id=entity['book'], range_id=place_id, property_code='P67')  # Link to Reference
        insert_geom(entity_id=location_id, geom=entity['geom'], title=entity['title'])
        # data.append({"name": entity['name'], "date": entity['date'], "location_id": location_id})
        data.append({"name": entity['name'], "location_id": location_id})


def get_data(source):
    with open(source, encoding="utf8") as f:
        input = json.load(f)
        data = []
        for feature in input['features']:
            ####### Data for border lines
            # data.append(
            #     {'title': feature['properties']['title'] + ' ' + feature['properties']['year'],
            #      "name": feature['properties']['title'],
            #      'date': feature['properties']['year'],
            #      'book': feature['properties']['book'],
            #      'geom': feature['geometry']})
            data.append(
                {'title': feature['geometry']['title'],
                 'name': feature['geometry']['title'],
                 'geom': feature['geometry']})
        return data


def insert_entity(title, code, system_class, date):
    sql = """
        INSERT INTO model.entity (name, system_class, description, begin_from, end_from, class_code)
        VALUES (%(name)s, %(system_class)s, %(description)s, %(begin_from)s, %(end_from)s, %(code)s)
        RETURNING id;"""
    params = {'name': str(title).strip(),
              'system_class': system_class,
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


def insert_geom(entity_id, geom, title):
    # Test for valid geom
    sql = """
        SELECT st_isvalid(
            public.ST_SetSRID(public.ST_GeomFromGeoJSON(%(geojson)s),4326));"""
    cursor.execute(sql, {'geojson': json.dumps(geom)})
    if not cursor.execute:
        return "Invalid geom"
    shape = geom['type']
    shape_type = ""
    if shape == "Point":
        shape_type = "centerpoint"
    if shape == "LineString":
        shape_type = "polyline"
    if shape == "Polygon":
        shape_type = "area"

    sql = """INSERT INTO gis.{shape} (entity_id, name, description, type, geom) VALUES (
                            %(entity_id)s,
                            %(name)s,
                            %(description)s,
                            %(type)s,
                            public.ST_SetSRID(public.ST_GeomFromGeoJSON(%(geojson)s),4326))
                            RETURNING ID;
                        """.format(shape=shape if shape != 'line' else 'linestring')

    cursor.execute(sql, {'entity_id': entity_id,
                         'name': title,
                         # add sanitize if included in OA
                         'type': shape_type,
                         'description': "",
                         'geojson': json.dumps(geom)})
    conn.commit()


def datetime64_to_timestamp(date: numpy.datetime64):
    if not date:
        return None
    string = str(date)
    postfix = ''
    if string.startswith('-') or string.startswith('0000'):
        string = string[1:]
        postfix = ' BC'
    parts = string.split('-')
    year = int(parts[0]) + 1 if postfix else int(parts[0])
    month = int('01')
    day = int('01')
    return format(year, '04d') + '-' + format(month, '02d') + '-' + format(day, '02d') + postfix


gis_import()
