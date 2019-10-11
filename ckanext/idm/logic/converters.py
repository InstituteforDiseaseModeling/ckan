# encoding: utf-8

import hashlib
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
            data[(u'maintainer',)] = user[u'fullname']
            email = None

            expected_hash = user[u'email_hash'] if user.get(u'email_hash') else None
            has_context_user = context.get(u'user_obj') and hasattr(context[u'user_obj'], u'email')

            # Determine email
            if user.get(u'email'):
                email = _validate_email(user[u'email'], expected_hash)

            if not email and has_context_user:
                email = _validate_email(context[u'user_obj'].email, expected_hash)

            if not email:
                # If email is not available directly, guess it by attaching the same domain as a current user.
                my_user = logic.get_action(u'user_show')(context, {u'id': context[u'user']})
                domain = my_user[u'email'].split(u'@')[1]
                email = u'{}@{}'.format(data[(u'maintainer_email',)], domain)
                _validate_email(email, expected_hash, raise_exception=True)

            data[(u'maintainer_email',)] = email

        except logic.NotFound as e:
            raise Invalid(_(u'Enter a username, an email or a contact (e.g. First Last <alias@server.org>).'))

    return data[key]


def _validate_email(email, expected_hash, raise_exception=False):
    if not expected_hash:
        raise ValueError(u"Expected email hash is not available.")

    is_hash_ok = _hash_email(email) == expected_hash
    
    if raise_exception and not is_hash_ok:
        raise Invalid(u"User email is missing or it doesn't match the expected value.".format(email))

    return email if is_hash_ok else None


def _hash_email(email):
    try:
        # This hashing code is from the ckan core
        e = email.strip().lower().encode(u'utf8')
        email_hash = hashlib.md5(e).hexdigest()
    except Exception as e:
        email_hash = None

    return email_hash
