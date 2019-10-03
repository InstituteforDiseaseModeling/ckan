# encoding: utf-8

import re
import ckan.logic as logic

from ckan.common import _
from ckan.plugins.toolkit import Invalid
from email.utils import parseaddr
from ckanext.idm.logic.locations import get_location_geometry


def set_spatial_to_location_geometry(key, data, errors, context):
    location = data[(u'location',)]
    spatial_mode = data[(u'spatial_mode',)]

    # TODO: Remove after issue #63 is fixed (this is a workaround for issue #55).
    if isinstance(spatial_mode, list) and len(spatial_mode) > 0:
        spatial_mode = spatial_mode[0]

    # Note, when spatial mode is not checked, spatial_mode is either an empty list or an object of type Missing.
    if spatial_mode != u'manual':
        data[(u'spatial',)] = get_location_geometry(location)

    return data[key]


def set_maintainer(key, data, errors, context):
    value = data[key].strip()
    has_email = re.match(ur'[^@]+@[^@]+\.[^@]+', value)
    if has_email:
        if u'<' in value and u'>' in value:
            data[(u'maintainer',)], data[(u'maintainer_email',)] = parseaddr(value)
        else:
            email = value.replace(u' ', u'')
            if context.get(u'package') is None or context[u'package'].maintainer_email != email:
                data[(u'maintainer',)] = email
            else:
                data[(u'maintainer',)] = context[u'package'].maintainer
    else:
        try:
            user = logic.get_action(u'user_show')(context, {u'id': value})
            data[(u'maintainer_email',)] = user[u'email']
            data[(u'maintainer',)] = user[u'fullname']
        except logic.NotFound as e:
            raise Invalid(_(u'Enter a username, an email or a contact (e.g. First Last <alias@server.org>).'))

    return data[key]


