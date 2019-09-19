# encoding: utf-8

from nose.tools import assert_equals, assert_raises
from ckan.common import config
from ckan.plugins.toolkit import get_validator, Invalid
from ckan import plugins
from ckan.tests import helpers


class TestValidators(helpers.FunctionalTestBase):

    @classmethod
    def teardown_class(cls):
        if plugins.plugin_loaded(u'idm'):
            plugins.unload(u'idm')

    def reload_idm(self, key=u'', value=u''):
        config[key] = value
        if plugins.plugin_loaded(u'idm'):
            plugins.unload(u'idm')
        plugins.load(u'idm')

    '''
    most set these in the config
    ckan.range_max_date=2020/12/31
    ckan.range_min_date=1950/01/01
    ckan.acquisition_max_date=2019/12/31
    ckan.acquisition_min_date=2019/01/01
    '''

    def test_reasonable_range_date_mindate(self):
        v = get_validator(u'reasonable_range_date')
        assert_raises(Invalid, v, u'1949/12/31')

    def test_reasonable_range_date_maxdate(self):
        v = get_validator(u'reasonable_range_date')
        assert_raises(Invalid, v, u'2021/01/01')

    def test_reasonable_range_date_upperbound(self):
        v = get_validator(u'reasonable_range_date')
        assert_equals(u'2020/12/31', v(u'2020/12/31'))

    def test_reasonable_range_date_lowerbound(self):
        v = get_validator(u'reasonable_range_date')
        assert_equals(u'1950/01/01', v(u'1950/01/01'))
