#!/usr/bin/env python
# encoding: utf-8

import os

import ckan.plugins as p
import ckan.plugins.toolkit as tk
import ckanext.idm.logic.action as action

from ckan.lib.plugins import DefaultTranslation
from flask import Blueprint

import ckanext.idm.logic.action as action
import ckanext.idm.views.api as view
import helpers as hlp


HERE = os.path.abspath(os.path.dirname(__file__))
I18N_DIR = os.path.join(HERE, u'i18n')

class IdmPlugin(p.SingletonPlugin, DefaultTranslation):
    p.implements(p.IBlueprint)
    p.implements(p.IActions)
    p.implements(p.ITranslation)
    p.implements(p.IConfigurer)
    p.implements(p.ITemplateHelpers, inherit=False)

    # IBlueprint

    def get_blueprint(self):
        u'''Return a Flask Blueprint object to be registered by the app.'''

        # Create Blueprint for plugin
        blueprint = Blueprint(self.name, self.__module__)
        blueprint.template_folder = u'templates'
        # Add plugin url rules to Blueprint object
        rules = [
            (u'/idm/publisher/autocomplete', u'publisher_autocomplete', view.publisher_autocomplete),
            (u'/idm/tag/autocomplete', u'tag_autocomplete', view.tag_autocomplete),
        ]
        for rule in rules:
            blueprint.add_url_rule(*rule)

        return blueprint

    # IActions

    def get_actions(self):
        return ({
            u'publisher_autocomplete': action.publisher_autocomplete})

    # ITranslation

    def i18n_directory(self):
        return I18N_DIR

    def i18n_domain(self):
        return u'ckan'

    # IConfigurer

    def update_config(self, config):
        p.toolkit.add_template_directory(config, 'templates')
        p.toolkit.add_public_directory(config, 'public')

    # ITemplateHelpers

    def get_helpers(self):
        return {
            'get_diseases_choices': hlp.get_diseases_choices
            #'get_resource_types_choices': hlp.get_resource_types_choices
            # 'get_topics_choices': hlp.get_topics_choices
            , 'get_country_choices': hlp.get_country_choices
            #, 'get_publisher_choices': hlp.get_publisher_choices
        }


