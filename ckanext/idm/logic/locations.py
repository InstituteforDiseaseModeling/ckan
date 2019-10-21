# encoding: utf-8

import json
import os
import zipfile

# TODO: Optimize loading of locations (import into db or load to some session object).
WORLD = u'World'
WORLD_GEOMETRY = u'{ "type": "Polygon", "coordinates": [ [ [ -180, -90 ], [ -180, 90 ], [ 180, 90 ], [ 180, -90 ], [ -180, -90 ] ] ] }'

SEARO = u'Asia:SEARO'
SEARO_GEOMETRY = u'{ "type": "Polygon", "coordinates": [ [ [ 68, 5 ], [ 68, 36 ], [ 105, 36 ], [ 105, 5 ], [ 68, 5 ] ] ] }'


def load_locations():
    features = _load()
    countries = [c[u'properties'][u'path'] for c in features]
    countries = sorted(countries)

    return [WORLD, SEARO] + countries


def get_location_geometry(location):
    if location.lower() == WORLD.lower():
        return WORLD_GEOMETRY
    elif location.lower() == SEARO.lower():
        return SEARO_GEOMETRY

    features = _load()
    geos = [c[u'geometry'] for c in features if c[u'properties'][u'path'] == location]
    geo = str(geos[0] if len(geos) > 0 else u'')
    geo = geo.replace(u'u\'', u'"')
    geo = geo.replace(u'\'', u'"')

    return geo


def _load():
    idm_dir = os.path.dirname(__file__)
    locations_zip = os.path.join(idm_dir, ur'../assets/geo/locations.zip')
    with zipfile.ZipFile(locations_zip, u'r') as zf:
        file_name = zf.namelist()[0]
        with zf.open(file_name, u'r') as cf:
            features = json.load(cf)[u'features']

    return features
