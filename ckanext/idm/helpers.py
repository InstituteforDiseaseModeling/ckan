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
#     return _get_vocabilary('resource_type', _create_resource_types)


def get_diseases():
    return _get_vocabilary('disease', _create_diseases)


def _to_choices_helper_format(list):
    choices = [{'value': str(v).lower(), 'label': v} for v in list]

    return choices

# def _create_resource_types():
#     _create_tag_vocabilary('resource_type', (u'data', u'doc', u'paper', u'code'))
#

def _create_diseases():
    _create_tag_vocabilary('disease', (u'Any', u'Malaria', u'Cholera', u'Typhoid', u'Polio', u'TB', u'HIV', u'Measles', u'Ebola', u'Pneumonia', u'HAT'))


def _create_tag_vocabilary(vocabulary_name, values_tuple):
    user = tk.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    try:
        data = {'id': vocabulary_name}
        tk.get_action('vocabulary_show')(context, data)
        logging.info("Example genre vocabulary already exists, skipping.")
    except tk.ObjectNotFound:
        logging.info("Creating vocab {}".format(vocabulary_name))
        data = {'name': vocabulary_name}
        vocab = tk.get_action('vocabulary_create')(context, data)
        for tag in (values_tuple):
            logging.info(
                    "Adding tag {0} to vocab 'resource_type'".format(tag))
            data = {'name': tag, 'vocabulary_id': vocab['id']}
            tk.get_action('tag_create')(context, data)


def _get_vocabilary(vocabulary_name, create_values_func):
    """
    Return the list of resource_types from the resource_type vocabulary.
    """
    create_values_func()
    try:
        resource_type = tk.get_action('tag_list')(data_dict={'vocabulary_id': vocabulary_name})
        return resource_type
    except tk.ObjectNotFound:
        return None

