# encoding: utf-8

import re
import ckan.logic as logic

from ckan.common import _
from ckan.plugins.toolkit import Invalid
from email.utils import parseaddr
from ckanext.idm.logic.locations import get_location_geometry


def set_spatial_to_location_geometry(key, data, errors, context):
    location = data[(u'location',)]
    if data[(u'spatial_mode',)] != u'manual':
        data[(u'spatial',)] = get_location_geometry(location)

    return data[key]


def set_maintainer(key, data, errors, context):
    value = data[key].strip()
    has_email = re.match(r'[^@]+@[^@]+\.[^@]+', value)
    if has_email:
        if '<' in value and '>' in value:
            data[(u'maintainer',)], data[(u'maintainer_email',)] = parseaddr(value)
        else:
            email = value.replace(' ', '')
            if context.get('package') is None or context['package'].maintainer_email != email:
                data[(u'maintainer',)] = email
            else:
                data[(u'maintainer',)] = context['package'].maintainer
    else:
        try:
            user = logic.get_action('user_show')(context, {'id': value})
            data[(u'maintainer_email',)] = user['email']
            data[(u'maintainer',)] = user['fullname']
        except logic.NotFound as e:
            raise Invalid(_(u'Maintainer is wrong'.format()))

    return data[key]


