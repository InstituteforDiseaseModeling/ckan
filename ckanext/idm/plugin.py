import logging
import os

import ckan.plugins as plugins
import ckan.plugins.toolkit as tk


group_type = u'group'

def create_tag_vocabilary(vocabulary_name, values_tuple):
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

def get_vocabilary_func(vocabulary_name, create_values_func):
    '''Return the list of resource_types from the resource_type vocabulary.'''
    create_values_func()
    try:
        resource_type = tk.get_action('tag_list')(data_dict={'vocabulary_id': vocabulary_name})
        return resource_type
    except tk.ObjectNotFound:
        return None


def create_resource_types():
    create_tag_vocabilary('resource_type', (u'data', u'doc', u'paper', u'code'))
    #
    # user = tk.get_action('get_site_user')({'ignore_auth': True}, {})
    # context = {'user': user['name']}
    # try:
    #     data = {'id': 'resource_type'}
    #     tk.get_action('vocabulary_show')(context, data)
    #     logging.info("Example genre vocabulary already exists, skipping.")
    # except tk.ObjectNotFound:
    #     logging.info("Creating vocab 'resource_type'")
    #     data = {'name': 'resource_type'}
    #     vocab = tk.get_action('vocabulary_create')(context, data)
    #     for tag in (u'data', u'doc', u'paper', u'code'):
    #         logging.info(
    #                 "Adding tag {0} to vocab 'resource_type'".format(tag))
    #         data = {'name': tag, 'vocabulary_id': vocab['id']}
    #         tk.get_action('tag_create')(context, data)


def get_resource_types():
    return get_vocabilary_func('resource_type', create_resource_types)
    # '''Return the list of resource_types from the resource_type vocabulary.'''
    # create_resource_types()
    # try:
    #     resource_type = tk.get_action('tag_list')(
    #             data_dict={'vocabulary_id': 'resource_type'})
    #     return resource_type
    # except tk.ObjectNotFound:
    #     return None


def create_diseases():
    create_tag_vocabilary('disease', (u'any', u'malaria', u'cholera', u'typhoid', u'polio', u'tb', u'hiv', u'measles', u'ebola', u'pneumonia', u'hat'))
    #
    # user = tk.get_action('get_site_user')({'ignore_auth': True}, {})
    # context = {'user': user['name']}
    # try:
    #     data = {'id': 'disease'}
    #     tk.get_action('vocabulary_show')(context, data)
    #     logging.info("Example genre vocabulary already exists, skipping.")
    # except tk.ObjectNotFound:
    #     logging.info("Creating vocab 'disease'")
    #     data = {'name': 'disease'}
    #     vocab = tk.get_action('vocabulary_create')(context, data)
    #     for tag in (u'any', u'malaria', u'cholera', u'typhoid', u'polio', u'tb', u'hiv', u'measles', u'ebola', u'pneumonia', u'hat'):
    #         logging.info(
    #                 "Adding tag {0} to vocab 'disease'".format(tag))
    #         data = {'name': tag, 'vocabulary_id': vocab['id']}
    #         tk.get_action('tag_create')(context, data)


def get_diseases():
    return get_vocabilary_func('disease', create_diseases)
    # '''Return the list of diseases from the disease vocabulary.'''
    # create_diseases()
    # try:
    #     disease = tk.get_action('tag_list')(
    #             data_dict={'vocabulary_id': 'disease'})
    #     return disease
    # except tk.ObjectNotFound:
    #     return None

class IdmPlugin(plugins.SingletonPlugin, tk.DefaultDatasetForm): #, tk.DefaultGroupForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IDatasetForm, inherit=False)
    plugins.implements(plugins.ITemplateHelpers, inherit=False)
    #plugins.implements(plugins.IGroupForm, inherit=False)

    # These record how many times methods that this plugin's methods are
    # called, for testing purposes.
    num_times_new_template_called = 0
    num_times_read_template_called = 0
    num_times_edit_template_called = 0
    num_times_search_template_called = 0
    num_times_history_template_called = 0
    num_times_package_form_called = 0
    num_times_check_data_dict_called = 0
    num_times_setup_template_variables_called = 0

    # IConfigurer

    def update_config(self, config_):

        for k, v in config_.items():
            if type(v) == str:
                config_[k] = v.replace(os.sep, '/')

        tk.add_template_directory(config_, './ckanext/idm/templates')
        #tk.add_public_directory(config_, 'public')
        #tk.add_resource('fanstatic', 'idm')

    def get_helpers(self):
        return {'disease': get_diseases, 'resource_type': get_resource_types}

    def is_fallback(self):
        return True
    

    def package_types(self):
        return []

    def _modify_package_schema(self, schema):
        schema.update({
                'disease': [tk.get_validator('ignore_missing'),
                    tk.get_converter('convert_to_tags')('disease')]
                })
        # # Add our custom_test metadata field to the schema, this one will use
        # # convert_to_extras instead of convert_to_tags.
        # schema.update({
        #         'custom_text': [tk.get_validator('ignore_missing'),
        #             tk.get_converter('convert_to_extras')]
        #         })
        # Add our custom_resource_text metadata field to the schema
        schema['resources'].update({
                'custom_resource_text' : [ tk.get_validator('ignore_missing') ]
                })

        schema.update({
                'resource_type': [tk.get_validator('ignore_missing'),
                    tk.get_converter('convert_to_tags')('resource_type')]
                })

        return schema

    def create_package_schema(self):
        schema = super(IdmPlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        schema = super(IdmPlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def show_package_schema(self):
        schema = super(IdmPlugin, self).show_package_schema()

        # Don't show vocab tags mixed in with normal 'free' tags
        # (e.g. on dataset pages, or on the search page)
        schema['tags']['__extras'].append(tk.get_converter('free_tags_only'))

        # Add our custom disease metadata field to the schema.
        schema.update({
            'disease': [
                tk.get_converter('convert_from_tags')('disease'),
                tk.get_validator('ignore_missing')]
            })

        # # Add our custom_text field to the dataset schema.
        # schema.update({
        #     'custom_text': [tk.get_converter('convert_from_extras'),
        #         tk.get_validator('ignore_missing')]
        #     })

        schema['resources'].update({
                'custom_resource_text' : [ tk.get_validator('ignore_missing') ]
            })
        return schema


    # These methods just record how many times they're called, for testing
    # purposes.
    # TODO: It might be better to test that custom templates returned by
    # these methods are actually used, not just that the methods get
    # called.

    def setup_template_variables(self, context, data_dict):
        IdmPlugin.num_times_setup_template_variables_called += 1
        return super(IdmPlugin, self).setup_template_variables(
                context, data_dict)

    def new_template(self):
        IdmPlugin.num_times_new_template_called += 1
        return super(IdmPlugin, self).new_template()

    def read_template(self):
        IdmPlugin.num_times_read_template_called += 1
        return super(IdmPlugin, self).read_template()

    def edit_template(self):
        IdmPlugin.num_times_edit_template_called += 1
        return super(IdmPlugin, self).edit_template()

    def search_template(self):
        IdmPlugin.num_times_search_template_called += 1
        return super(IdmPlugin, self).search_template()

    def history_template(self):
        IdmPlugin.num_times_history_template_called += 1
        return super(IdmPlugin, self).history_template()

    def package_form(self):
        IdmPlugin.num_times_package_form_called += 1
        return super(IdmPlugin, self).package_form()

    # check_data_dict() is deprecated, this method is only here to test that
    # legacy support for the deprecated method works.
    def check_data_dict(self, data_dict, schema=None):
        IdmPlugin.num_times_check_data_dict_called += 1
    #
    # # IGroupForm
    #
    # def group_types(self):
    #     return ('group', 'team')
    #
    # def group_form(self):
    #     return 'group/group_form.html'


