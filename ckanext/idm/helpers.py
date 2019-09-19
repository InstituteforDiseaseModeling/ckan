#!/usr/bin/env python
# encoding: utf-8

import re
import datetime
import pytz
import json
import logging

import ckan.plugins.toolkit as tk


# def get_resource_types_choices(field):
#     return _to_choices_helper_format(get_resource_types())
#

def get_diseases_choices(field):
    return _to_choices_helper_format(get_diseases())

#
# def get_topics_choices(field):
#     return _to_choices_helper_format(get_topics())

#
# def get_resource_types():
#     return _get_vocabilary(u'resource_type', _create_resource_types)


def get_diseases():
    return _get_vocabilary(u'disease', _create_diseases)


def _to_choices_helper_format(list):
    choices = [{u'value': str(v), u'label': v} for v in list]

    return choices

# def _create_resource_types():
#     _create_tag_vocabilary(u'resource_type', (u'data', u'doc', u'paper', u'code'))
#

# TODO storie it in a file and support added/removed/updated scenarios.
def _create_diseases():
    _create_tag_vocabilary(u'disease', (u'Any', u'Malaria', u'Cholera', u'Typhoid', u'Polio', u'TB', u'HIV', u'Measles', u'Ebola', u'Pneumonia', u'HAT'))


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


def _get_vocabilary(vocabulary_name, create_values_func):
    """
    Return the list of resource_types from the resource_type vocabulary.
    """
    create_values_func()
    try:
        resource_type = tk.get_action(u'tag_list')(data_dict={u'vocabulary_id': vocabulary_name})
        return resource_type
    except tk.ObjectNotFound:
        return None

