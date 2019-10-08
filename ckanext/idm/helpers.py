# encoding: utf-8

import logging

import ckan.plugins.toolkit as tk
import ckan.model as model

from ckan.lib.helpers import core_helper, url_for
from six import text_type
from webhelpers.html import literal, tags


def get_diseases_choices(field):
    return _to_choices_helper_format(get_diseases())


def get_diseases():
    return _get_vocabilary(u'disease')


def _to_choices_helper_format(list):
    choices = [{u'value': str(v), u'label': v} for v in list]

    return choices


def _create_tag_vocabilary(vocabulary_name, values_tuple):
    user = tk.get_action(u'get_site_user')({u'ignore_auth': True}, {})
    context = {u'user': user[u'name']}
    try:
        data = {u'id': vocabulary_name}
        tk.get_action(u'vocabulary_show')(context, data)
        logging.info(u"Example genre vocabulary already exists, skipping.")
    except tk.ObjectNotFound:
        logging.info(u"Creating vocab {}".format(vocabulary_name))
        data = {u'name': vocabulary_name}
        vocab = tk.get_action(u'vocabulary_create')(context, data)
        for tag in (values_tuple):
            logging.info(
                    u"Adding tag {0} to vocab 'resource_type'".format(tag))
            data = {u'name': tag, u'vocabulary_id': vocab[u'id']}
            tk.get_action(u'tag_create')(context, data)


def _get_vocabilary(vocabulary_name):
    """Return the list of resource_types from the resource_type vocabulary."""
    try:
        resource_type = tk.get_action(u'tag_list')(data_dict={u'vocabulary_id': vocabulary_name})
        return resource_type
    except tk.ObjectNotFound:
        return None


@core_helper
def gravatar(email_hash, size=100, default=None):
    i = int(email_hash[0], 16) % 20 + 1
    img_tag = u'''<img src="/images/user-logo/tux-{}.png" width="{}" height="{}" alt="Tux" />'''
    return literal(img_tag.format(i, size, size))


@core_helper
def linked_gravatar(email_hash, size=100, default=None):
    return literal(gravatar(email_hash, size, default))


@core_helper
def linked_user(user, maxlength=0, avatar=20):
    if not isinstance(user, model.User):
        user_name = text_type(user)
        user = model.User.get(user_name)
        if not user:
            return user_name
    if user:
        name = user.name if model.User.VALID_NAME.match(user.name) else user.id
        displayname = user.display_name

        if maxlength and len(user.display_name) > maxlength:
            displayname = displayname[:maxlength] + '...'

        return tags.literal(u'{icon} {link}'.format(
            icon=gravatar(
                email_hash=user.email_hash,
                size=avatar
            ),
            link=tags.link_to(
                displayname,
                url_for('user.read', id=name)
            )
        ))
