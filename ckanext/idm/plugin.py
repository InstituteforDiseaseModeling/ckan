#!/usr/bin/env python
# encoding: utf-8

import os

import ckan.plugins as plugins
import ckan.plugins.toolkit as tk
from ckan.lib.plugins import DefaultTranslation

import helpers as hlp

HERE = os.path.abspath(os.path.dirname(__file__))
I18N_DIR = os.path.join(HERE, u'i18n')

class IdmPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers, inherit=False)

    def i18n_directory(self):
        return I18N_DIR

    def i18n_domain(self):
        return u'ckan'

    def update_config(self, config):
        plugins.toolkit.add_template_directory(config, 'templates')
        plugins.toolkit.add_public_directory(config, 'public')

    def get_helpers(self):
        return {
            'get_diseases_choices': hlp.get_diseases_choices
            #'get_resource_types_choices': hlp.get_resource_types_choices
            # 'get_topics_choices': hlp.get_topics_choices
            , 'get_country_choices': hlp.get_country_choices
            , 'get_publisher_choices': hlp.get_publisher_choices
        }


