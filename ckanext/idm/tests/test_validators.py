# encoding: utf-8

from nose.tools import assert_equals, assert_raises
from ckan.common import config
from ckan.plugins.toolkit import get_validator, Invalid
from ckan import plugins
from ckan.tests import helpers
from datetime import date, timedelta
from ckanext.idm.logic import validators

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

    def test_acquisition_today(self):
        self.reload_idm(u'ckan.acquisition_max_date', '')
        reload(validators)
        v = get_validator(u'reasonable_acquisition_date')
        today = date.today().strftime(u'%Y/%m/%d')
        assert_equals(today, v(today))

    def test_acquisition_future(self):
        self.reload_idm(u'ckan.acquisition_max_date', u'')
        reload(validators)
        v = get_validator(u'reasonable_acquisition_date')
        tomorrow = (date.today() + timedelta(days=1)).strftime(u'%Y/%m/%d')
        assert_raises(Invalid, v, tomorrow)

    def test_acquisition_mindate(self):
        self.reload_idm(u'ckan.acquisition_min_date', u'')
        reload(validators)
        v = get_validator(u'reasonable_acquisition_date')
        crazydate = u'1800/01/01'
        assert_raises(Invalid, v, crazydate)

    def test_acquisition_yesterday(self):
        self.reload_idm(u'ckan.acquisition_min_date', u'')
        self.reload_idm(u'ckan.acquisition_max_date', u'')
        reload(validators)
        v = get_validator(u'reasonable_acquisition_date')
        yesterday = (date.today() + timedelta(days=-1)).strftime(u'%Y/%m/%d')
        assert_equals(yesterday, v(yesterday))
