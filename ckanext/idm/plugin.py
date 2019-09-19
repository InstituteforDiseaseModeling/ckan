# encoding: utf-8

import os
from collections import OrderedDict

import ckan.plugins as p

from ckan.lib.plugins import DefaultTranslation
from flask import Blueprint

import ckanext.idm.logic.action.create as create
import ckanext.idm.logic.action.get as get
import ckanext.idm.logic.auth.create as auth_create
import ckanext.idm.logic.validators as validators
import ckanext.idm.logic.converters as converters
import ckanext.idm.views.api as view
import ckanext.idm.helpers as hlp


HERE = os.path.abspath(os.path.dirname(__file__))
I18N_DIR = os.path.join(HERE, u'i18n')

class IdmPlugin(p.SingletonPlugin, DefaultTranslation):
    p.implements(p.IFacets)
    p.implements(p.IBlueprint)
    p.implements(p.IActions)
    p.implements(p.ITranslation)
    p.implements(p.IConfigurer)
    p.implements(p.ITemplateHelpers, inherit=False)
    p.implements(p.IValidators)
    p.implements(p.IAuthFunctions)

    # IFacets

    def dataset_facets(self, facets_dict, package_type):
        for key in facets_dict.keys():
            del facets_dict[key]

        #facets_dict_idm = OrderedDict()
        facets_dict[u'location'] = p.toolkit._(u'Location')
        facets_dict[u'disease'] = p.toolkit._(u'Disease')
        facets_dict[u'publisher'] = p.toolkit._(u'Publisher')
        facets_dict[u'res_format'] = p.toolkit._(u'Formats')
        facets_dict[u'tags'] = p.toolkit._(u'Tags')

        return facets_dict

    def group_facets(self, facets_dict, group_type, package_type):
        return self.dataset_facets(facets_dict, package_type)

    def organization_facets(self, facets_dict, organization_type, package_type):
        return self.dataset_facets(facets_dict, package_type)


    # IBlueprint

    def get_blueprint(self):
        u'''Return a Flask Blueprint object to be registered by the app.'''

        # Create Blueprint for plugin
        blueprint = Blueprint(self.name, self.__module__)
        blueprint.template_folder = u'templates'
        # Add plugin url rules to Blueprint object
        rules = [
            (u'/idm/location/autocomplete',  u'location_autocomplete',  view.location_autocomplete),
            (u'/idm/publisher/autocomplete', u'publisher_autocomplete', view.publisher_autocomplete),
            (u'/idm/tag/autocomplete', u'tag_autocomplete', view.tag_autocomplete),
        ]
        for rule in rules:
            blueprint.add_url_rule(*rule)

        return blueprint

    # IActions

    def get_actions(self):
        return ({
            u'location_autocomplete':  get.location_autocomplete,
            u'publisher_autocomplete': get.publisher_autocomplete,
            u'resource_create': create.resource_create,
            u'group_list_authz': get.group_list_authz,
        })

    # ITranslation

    def i18n_directory(self):
        return I18N_DIR

    def i18n_domain(self):
        return u'ckan'

    # IConfigurer

    def update_config(self, config):
        p.toolkit.add_template_directory(config, u'templates')
        p.toolkit.add_public_directory(config, u'public')

    # ITemplateHelpers

    def get_helpers(self):
        return {
            u'get_diseases_choices': hlp.get_diseases_choices
            #'get_resource_types_choices': hlp.get_resource_types_choices
        }

    # IValidator

    def get_validators(self):
        return {
            u'reasonable_range_date': validators.reasonable_range_date,
            u'reasonable_acquisition_date': validators.reasonable_acquisition_date,
            u'temporal_range': validators.temporal_range,
            u'set_spatial_to_location_geometry': converters.set_spatial_to_location_geometry,
        }

    # IAuthFunctions

    def get_auth_functions(self):
        return {u'member_create': auth_create.member_create}

