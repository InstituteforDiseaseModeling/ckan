# encoding: utf-8

'''API functions for searching for and getting data from CKAN.'''

import json
import logging
import os
import zipfile

import sqlalchemy

import ckan.logic as logic
import ckan.authz as authz
import ckan.lib.dictization.model_dictize as model_dictize

from ckanext.idm.logic.locations import load_locations

log = logging.getLogger(u'ckan.logic')
_check_access = logic.check_access
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
    default_list = load_locations()

    #[u'World', u'Africa:Zambia', u'Africa:Kenya', u'Asia:Pakistan']

    results = _extra_autocomplete(context, data_dict, u'location', default_list)

    return results


@logic.validate(logic.schema.default_autocomplete_schema)
def publisher_autocomplete(context, data_dict):
    # TODO: load the list of publishers from a file
    default_list = [u'WHO', u'NOAA', u'WorldPop', u'WorldClim', u'DHS', u'UNICEF', u'CDC', ]

    # TODO:
    # - Only include datasets which a user has right to see
    # - Add a predefined list of data sources
    # - Consider capturing publishers a new group type
    results = _extra_autocomplete(context, data_dict, u'publisher', default_list)

    return results


def _extra_autocomplete(context, data_dict, key, default_list=[]):
    model = context[u'model']
    session = context[u'session']

    #_check_access(u'package_update', context, data_dict)
    q = data_dict[u'q']
    limit = data_dict.get(u'limit', 5)

    like_q = u'%' + q + u'%'

    query = (
        session
            .query(model.PackageExtra.value, _func.count(model.PackageExtra.value).label(u'total'))
            .filter(_and_(model.PackageExtra.key == key, model.PackageExtra.state == u'active',))
            .filter(model.PackageExtra.value.ilike(like_q))
            .group_by(model.PackageExtra.value)
            .order_by(u'total DESC')
            .limit(limit))

    results_1 = [package_extra.value for package_extra in query]

    results_2 =  [v for v in default_list if q.lower() in v.lower()]

    results = list(set((results_1 + results_2)))
    results = sorted(results)

    return results


def group_list_authz(context, data_dict):
    '''Return the list of groups that the user is authorized to edit.

    :param available_only: remove the existing groups in the package
      (optional, default: ``False``)
    :type available_only: bool

    :param am_member: if ``True`` return only the groups the logged-in user is
      a member of, otherwise return all groups that the user is authorized to
      edit (for example, sysadmin users are authorized to edit all groups)
      (optional, default: ``False``)
    :type am_member: bool

    :returns: list of dictized groups that the user is authorized to edit
    :rtype: list of dicts

    '''
    model = context[u'model']
    user = context[u'user']
    available_only = data_dict.get(u'available_only', False)
    # am_member = data_dict.get(u'am_member', False)

    _check_access(u'group_list_authz', context, data_dict)

    # sysadmin = authz.is_sysadmin(user)
    roles = authz.get_roles_with_permission(u'manage_group')
    if not roles:
        return []
    user_id = authz.get_user_id_for_username(user, allow_none=True)
    if not user_id:
        return []

    # Allows any user to add any dataset to any topic.

    # if not sysadmin or am_member:
    #     q = model.Session.query(model.Member) \
    #         .filter(model.Member.table_name == 'user') \
    #         .filter(model.Member.capacity.in_(roles)) \
    #         .filter(model.Member.table_id == user_id) \
    #         .filter(model.Member.state == 'active')
    #     group_ids = []
    #     for row in q.all():
    #         group_ids.append(row.group_id)

        if not group_ids:
            return []

    q = model.Session.query(model.Group) \
        .filter(model.Group.is_organization == False) \
        .filter(model.Group.state == u'active')

    # if not sysadmin or am_member:
    #     q = q.filter(model.Group.id.in_(group_ids))

    groups = q.all()

    if available_only:
        package = context.get(u'package')
        if package:
            groups = set(groups) - set(package.get_groups())

    group_list = model_dictize.group_list_dictize(groups, context)
    return group_list
