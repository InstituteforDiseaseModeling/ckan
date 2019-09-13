# encoding: utf-8
"""Tests for plugin.py."""
import nose.tools as nt
import ckanext.idm.helpers as idm_helper
import ckan.logic as logic
import ckan.model as model
import ckan.plugins as plugins
from ckan.common import config
from bs4 import BeautifulSoup
from ckan.tests import factories, helpers
import sys


class TestidmPlugins(helpers.FunctionalTestBase):

    expected_diseases = [
        u'Any',
        u'Cholera',
        u'Ebola',
        u'HAT',
        u'HIV',
        u'Malaria',
        u'Measles',
        u'Pneumonia',
        u'Polio',
        u'TB',
        u'Typhoid']

    expected_purposes = [
        u'data',
        u'project',
        u'paper'
    ]

    expected_topics = [
        u'Incidence Data',
        u'Mortality',
        u'Population',
        u'Shapefiles',
        u'Births',
        u'Climate',
        u'MICS - Multiple Indicator Cluster Surveys',
        u'VTS - Vertical Transmission cohort Study',
        u'SIAs -  Supplemental immunisation activity campaigns',
        u'PCCS - Post Campaign Coverage Surveys'
    ]

    expected_research_groups = [
        u'AMath',
        u'DDA',
        u'ECON',
        u'EPI',
        u'HAT',
        u'HIV',
        u'Malaria',
        u'Measles',
        u'MNCH',
        u'Polio',
        u'TB',
        u'Data Services'
    ]

    expected_resource_types = [
        u'data',
        u'code',
        u'doc',
        u'paper',
        u'provenance',
        u'other'
    ]

    basic_testdata = {
                      u'license_id': u'License not specified',
                      u'disease': u'Any',
                      u'acquisition_date': u'2019/01/01',
                      u'maintainer_email': u'fake@idm.org',
                      u'ext_startdate': u'2019/01/01',
                      u'ext_enddate': u'2019/01/02',
                      u'location': u'Africa',
                      u'purpose': u'paper',
                      u'publisher': u'WTO',
                      u'notes': u'this is a test'}
    @classmethod
    def _apply_config_changes(cls, cfg):
        cfg[u'ckan.plugins'] = u'idm scheming_datasets'

    @classmethod
    def teardown_class(cls):
        if plugins.plugin_loaded(u'idm'):
            plugins.unload(u'idm')
        if plugins.plugin_loaded(u'scheming_datasets'):
            plugins.unload(u'scheming_datasets')
        helpers.reset_db()

    def create_topics(self, name=None):
        topics = helpers.call_action(u'group_list')
        user = factories.User()
        context = {
            u'user': user[u'name'],
            u'ignore_auth': True,
        }
        if name is not None:
            result = helpers.call_action(u'group_create',
                                         context=context,
                                         name=str(name).lower().replace(u' ', u'-'),
                                         title=name)
            nt.assert_equal(name, result[u'title'])
            return
        for t in self.expected_topics:
            if t not in topics:
                result = helpers.call_action(u'group_create',
                                             context=context,
                                             name=str(t).lower().replace(u' ', u'-'),
                                             title=t)
                nt.assert_equal(t, result[u'title'])

    def delete_topics(self):
        topics = helpers.call_action(u'organization_list')
        for t in self.expected_topics:
            if t in topics:
                helpers.call_action(u'group_delete',
                                    id=topics[u'id'])

    def create_research_groups(self, name=None):
        orgs = helpers.call_action(u'organization_list')
        user = factories.User()
        context = {
            u'user': user[u'name'],
            u'ignore_auth': True,
        }
        if name is not None:
            result = helpers.call_action(u'organization_create',
                                         context=context,
                                         name=str(name).lower().replace(u' ', u'-'),
                                         title=name)
            nt.assert_equal(name, result[u'title'])
            return
        for r in self.expected_research_groups:
            if r not in orgs:
                result = helpers.call_action(u'organization_create',
                                             context=context,
                                             name=str(r).lower().replace(u' ', u'-'),
                                             title=r)
                nt.assert_equal(r, result[u'title'])

    def delete_research_groups(self):
        orgs = helpers.call_action(u'organization_list')
        for r in self.expected_research_groups:
            if r in orgs:
                helpers.call_action(u'organization_delete',
                                    id=orgs[u'id'])

    def test_diseases(self):
        d = idm_helper.get_diseases()
        nt.assert_equal(set(self.expected_diseases), set(d))

    def test_create_purpose(self):
        testdata = self.basic_testdata.copy()
        testdata[u'name'] = sys._getframe().f_code.co_name
        for p in self.expected_purposes:
            testdata[u'purpose'] = p
            result = helpers.call_action(u'package_create',
                                         **testdata
                                         )
            nt.assert_equals(p, result[u'purpose'])
            helpers.call_action(u'package_delete', id=result[u'id'])

    def test_create_research_groups(self):
        self.create_research_groups()
        self.delete_research_groups()

    def test_create_topics(self):
        self.create_topics()
        self.delete_topics()

    def test_create_disease(self):
        testdata = self.basic_testdata.copy()
        testdata[u'name'] = sys._getframe().f_code.co_name
        for d in self.expected_diseases:
            testdata[u'disease'] = d
            result = helpers.call_action(u'package_create',
                                         **testdata
                                         )

            nt.assert_equals(d, result[u'disease'])
            helpers.call_action(u'package_delete', id=result[u'id'])

    def test_update_disease(self):
        testdata = self.basic_testdata.copy()
        testdata[u'name'] = sys._getframe().f_code.co_name
        testdata[u'disease'] = u'Any'
        result = helpers.call_action(u'package_create',
                                     **testdata
                                     )
        nt.assert_equals(u'Any', result[u'disease'])
        testdata[u'disease'] = u'Polio'
        result = helpers.call_action(u'package_update',
                                     **testdata
                                     )
        nt.assert_equals(u'Polio', result[u'disease'])
        helpers.call_action(u'package_delete', id=result[u'id'])

    def test_create_resource_type(self):
        for rt in self.expected_resource_types:
            result = helpers.call_action(u'package_create',
                                         name=u'test_resource_type_package',
                                         license_id=u'License not specified',
                                         disease=u'Any',
                                         acquisition_date=u'2019/01/01',
                                         maintainer_email=u'fake@idm.org',
                                         ext_startdate=u'2019/01/01',
                                         ext_enddate=u'2019/01/02',
                                         location=u'Africa',
                                         purpose=u'paper',
                                         publisher=u'WTO',
                                         notes=u'this is a test',
                                         resources=[{
                                             u'url': u'http://idm.com/',
                                             u'name': u'testdata',
                                             u'purpose': rt
                                         }]
                                         )
            nt.assert_equals(rt, result[u'resources'][0]['purpose'])
            helpers.call_action(u'package_delete', id=result[u'id'])

    def test_get_dataset(self):
        testdata = self.basic_testdata.copy()
        testdata[u'name'] = sys._getframe().f_code.co_name
        testdata[u'disease'] = u'HIV'
        app = helpers._get_test_app()
        result = helpers.call_action(u'package_create',
                                     **testdata
                                     )
        response = app.get(u'/dataset/'+result[u'name'])
        response_html = BeautifulSoup(response.body)
        disease = [node.find(u'td').text for node in response_html.find_all(u'tr')
                   if u'Disease' in node.text][0]
        nt.assert_equals(u'HIV', str(disease))
        helpers.call_action(u'package_delete', id=result[u'id'])

    def test_get_dataset_by_research_group(self):
        testdata = self.basic_testdata.copy()
        testdata[u'name'] = sys._getframe().f_code.co_name
        self.create_research_groups(u'HIV')
        testdata[u'owner_org'] = u'hiv'
        app = helpers._get_test_app()
        result = helpers.call_action(u'package_create',
                                     **testdata)
        response = app.get(u'/organization/hiv')
        response_html = BeautifulSoup(response.body)
        nt.assert_equals(len([node for node in response_html.find_all(u'a')
                              if testdata[u'name'] in node.text]), 1)
        helpers.call_action(u'package_delete', id=result[u'id'])
        self.delete_research_groups()

    def test_location_autocomplete(self):
        testdata = self.basic_testdata.copy()
        testdata[u'name'] = sys._getframe().f_code.co_name
        testdata[u'location'] = u'badatadagoogoolo'
        helpers.call_action(u'package_create',
                            **testdata)
        suggested_list = helpers.call_action(
            u'location_autocomplete', context={u'ignore_auth': False}, q=u'bada'
        )
        assert u'badatadagoogoolo' in suggested_list

    def test_location_autocomplete_default(self):
        suggested_list = helpers.call_action(
            u'location_autocomplete', context={u'ignore_auth': False}, q=u'Taiw'
        )
        assert u'Asia:Taiwan' in suggested_list

    def test_publisher_autocomplete(self):
        testdata = self.basic_testdata.copy()
        testdata[u'name'] = sys._getframe().f_code.co_name
        testdata[u'publisher'] = u'Institute For Disease Modeling'
        helpers.call_action(u'package_create',
                            **testdata)
        suggested_list = helpers.call_action(
            u'publisher_autocomplete', context={u'ignore_auth': False}, q=u'Institute'
        )
        assert testdata[u'publisher'] in suggested_list

    def test_start_end_date(self):
        testdata = self.basic_testdata.copy()
        testdata[u'name'] = sys._getframe().f_code.co_name
        testdata[u'ext_startdate'] = u'2001/01/03'
        testdata[u'ext_enddate'] = u'2001/01/02'
        validated = False
        try:
            helpers.call_action(u'package_create',
                                **testdata)
        except logic.ValidationError as e:
            assert e.error_dict[u'ext_startdate']
            validated = True
        assert validated


    def test_acquisition_date(self):
        testdata = self.basic_testdata.copy()
        testdata[u'name'] = sys._getframe().f_code.co_name
        testdata[u'acquisition_date'] = u'1900/01/01'
        validated = False
        try:
            helpers.call_action(u'package_create',
                                **testdata)
        except logic.ValidationError as e:
            assert e.error_dict[u'acquisition_date']
            validated = True
        assert validated


