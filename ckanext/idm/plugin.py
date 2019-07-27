#!/usr/bin/env python
# encoding: utf-8

import os

import ckan.plugins as plugins
import ckan.plugins.toolkit as tk

import helpers as hlp


class IdmPlugin(plugins.SingletonPlugin):

    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers, inherit=False)

    def update_config(self, config):
        plugins.toolkit.add_template_directory(config, 'templates')

    def get_helpers(self):
        return {
            'get_diseases_choices': hlp.get_diseases_choices
            #'get_resource_types_choices': hlp.get_resource_types_choices
            # 'get_topics_choices': hlp.get_topics_choices
            , 'get_country_choices': hlp.get_country_choices
            , 'get_publisher_choices': hlp.get_publisher_choices
        }


