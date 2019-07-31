# encoding: utf-8
'''API functions for searching for and getting data from CKAN.'''

import json
import logging
import os
import zipfile

import sqlalchemy

import ckan.logic as logic
import ckan.logic.schema

log = logging.getLogger('ckan.logic')

_select = sqlalchemy.sql.select
_aliased = sqlalchemy.orm.aliased
_or_ = sqlalchemy.or_
_and_ = sqlalchemy.and_
_func = sqlalchemy.func
_desc = sqlalchemy.desc
_case = sqlalchemy.case
_text = sqlalchemy.text


@logic.validate(logic.schema.default_autocomplete_schema)
def location_autocomplete(context, data_dict):
    # TODO: use geojson file with dot-names including continent, country, province, district levels
    default_list = _load_locations()

    #['World', 'Africa:Zambia', 'Africa:Kenya', 'Asia:Pakistan']

    results = _extra_autocomplete(context, data_dict, 'location', default_list)

    return results


@logic.validate(logic.schema.default_autocomplete_schema)
def publisher_autocomplete(context, data_dict):
    # TODO: load the list of locations from a file
    default_list = ['WHO', 'NOAA', 'WorldPop', 'WorldClim']

    # TODO:
    # - Only include datasets which a user has right to see
    # - Add a predefined list of data sources
    # - Consider capturing publishers a new group type
    results = _extra_autocomplete(context, data_dict, 'publisher', default_list)

    return results


def _extra_autocomplete(context, data_dict, key, default_list=[]):
    model = context['model']
    session = context['session']

    #_check_access('package_update', context, data_dict)
    q = data_dict['q']
    limit = data_dict.get('limit', 5)

    like_q = u'%' + q + u'%'

    query = (
        session
            .query(model.PackageExtra.value, _func.count(model.PackageExtra.value).label('total'))
            .filter(_and_(model.PackageExtra.key == key, model.PackageExtra.state == 'active',))
            .filter(model.PackageExtra.value.ilike(like_q))
            .group_by(model.PackageExtra.value)
            .order_by('total DESC')
            .limit(limit))

    results_1 = [package_extra.value for package_extra in query]

    results_2 =  [v for v in default_list if q.lower() in v.lower()]

    results = sorted(results_1 + results_2)

    return results


def _load_locations():
    # TODO: Optimize loading of locations (import into db or load to some session object).
    idm_dir = os.path.dirname(__file__)
    locations_zip = os.path.join(idm_dir, r'../assets/geo/locations.zip')
    with zipfile.ZipFile(locations_zip, 'r') as zf:
        file_name = zf.namelist()[0]
        with zf.open(file_name, 'r') as cf:
            features = json.load(cf)['features']
            countries = [c['properties']['path'] for c in features]
            countries = sorted(countries)

    return ['World'] + countries
