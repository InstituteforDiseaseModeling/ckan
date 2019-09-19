# encoding: utf-8


import ckan.model as model
import ckan.logic.action.get as ag
#import ckan.views.api as va

from ckan.common import g, request
from ckan.logic import get_action
from ckan.views.api import _finish_ok, API_REST_DEFAULT_VERSION


def location_autocomplete(ver=API_REST_DEFAULT_VERSION):
    return _autocomplete(u'location_autocomplete')


def publisher_autocomplete(ver=API_REST_DEFAULT_VERSION):
    return _autocomplete(u'publisher_autocomplete')


def tag_autocomplete(ver=API_REST_DEFAULT_VERSION):
    q = request.args.get(u'incomplete', u'')
    limit = request.args.get(u'limit', 10)
    vocabulary_id = request.args.get(u'vocabulary_id', u'')
    tag_names = []

    if q:
        context = {
            u'model': model,
            u'session': model.Session,
            u'user': g.user,
            u'auth_user_obj': g.userobj
        }

        data_dict = {
            u'q': q,
            u'limit': limit,
            u'vocabulary_id': vocabulary_id
        }

        ag._check_access(u'tag_list', context, data_dict)
        tag_names = get_action(u'tag_list')(context, data_dict)

    resultSet = {
        u'ResultSet': {
            u'Result': [{u'Name': tag} for tag in tag_names]
        }
    }
    return _finish_ok(resultSet)


def _autocomplete(action_name):
    q = request.args.get(u'incomplete', u'')
    limit = request.args.get(u'limit', 5)
    formats = []
    if q:
        context = {u'model': model, u'session': model.Session,
                   u'user': g.user, u'auth_user_obj': g.userobj}
        data_dict = {u'q': q, u'limit': limit}
        formats = get_action(action_name)(context, data_dict)

    resultSet = {
        u'ResultSet': {
            u'Result': [{u'Format': format} for format in formats]
        }
    }
    return _finish_ok(resultSet)
