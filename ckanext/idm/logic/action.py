# encoding: utf-8
'''API functions for searching for and getting data from CKAN.'''

import logging

import sqlalchemy

import ckan.lib.dictization
import ckan.logic as logic
import ckan.logic.action
import ckan.logic.schema
import ckan.lib.navl.dictization_functions
import ckan.model as model
import ckan.plugins as plugins
import ckan.lib.search as search
import ckan.lib.plugins as lib_plugins

log = logging.getLogger('ckan.logic')

# Define some shortcuts
# Ensure they are module-private so that they don't get loaded as available
# actions in the action API.
_validate = ckan.lib.navl.dictization_functions.validate
_table_dictize = ckan.lib.dictization.table_dictize
_check_access = logic.check_access
NotFound = logic.NotFound
ValidationError = logic.ValidationError
_get_or_bust = logic.get_or_bust

_select = sqlalchemy.sql.select
_aliased = sqlalchemy.orm.aliased
_or_ = sqlalchemy.or_
_and_ = sqlalchemy.and_
_func = sqlalchemy.func
_desc = sqlalchemy.desc
_case = sqlalchemy.case
_text = sqlalchemy.text


@logic.validate(logic.schema.default_autocomplete_schema)
def publisher_autocomplete(context, data_dict):
    model = context['model']
    session = context['session']

    #_check_access('package_update', context, data_dict)
    q = data_dict['q']
    limit = data_dict.get('limit', 5)

    like_q = u'%' + q + u'%'

    # TODO:
    # - Only include datasets which a user has right to see
    # - Add a predefined list of data sources
    # - Consider capturing publishers a new group type

    query = (
        session
            .query(model.PackageExtra.value, _func.count(model.PackageExtra.value).label('total'))
            .filter(_and_(model.PackageExtra.key == 'publisher', model.PackageExtra.state == 'active',))
            .filter(model.PackageExtra.value.ilike(like_q))
            .group_by(model.PackageExtra.value)
             .order_by('total DESC')
             .limit(limit))

    return [package_extra.value.lower() for package_extra in query]

