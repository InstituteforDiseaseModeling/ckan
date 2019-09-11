# encoding: utf-8

import json
import os
import zipfile

# TODO: Optimize loading of locations (import into db or load to some session object).


def load_locations():
    features = _load()
    countries = [c['properties']['path'] for c in features]
    countries = sorted(countries)

    return ['World'] + countries


def get_location_geometry(location):
    features = _load()
    geos = [c['geometry'] for c in features if c['properties']['path'] == location]
    geo = str(geos[0] if len(geos) > 0 else '')
    geo = geo.replace('u\'', '"')
    geo = geo.replace('\'', '"')

    return geo


def _load():
    idm_dir = os.path.dirname(__file__)
    locations_zip = os.path.join(idm_dir, r'../assets/geo/locations.zip')
    with zipfile.ZipFile(locations_zip, 'r') as zf:
        file_name = zf.namelist()[0]
        with zf.open(file_name, 'r') as cf:
            features = json.load(cf)['features']

    return features
