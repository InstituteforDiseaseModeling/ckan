"""This module sets the behave environment"""
from behave import use_fixture
from utilities import driver


def before_tag(context, tag):
    context.driverpath = None
    context.browsertype = context.config.userdata[u'browser']
    context.server = context.config.userdata[u'server']
    context.relative_url = context.config.userdata[u'relative_url']
    context.params = context.config.userdata[u'params']
    context.logpath = context.config.userdata[u'logpath']
    context.timeout = int(context.config.userdata[u'timeout'])
    context.driver_version = context.config.userdata[u'driver_version']
    context.postgres_user = context.config.userdata[u'postgres_user']
    context.postgres_pass = context.config.userdata[u'postgres_pass']
    context.postgres_host = context.config.userdata[u'postgres_host']
    context.postgres_port = context.config.userdata[u'postgres_port']
    context.postgres_db = context.config.userdata[u'postgres_db']
    context.ckan_user = context.config.userdata[u'ckan_user']
    context.ckan_password = context.config.userdata[u'ckan_password']
    context.redis_server = context.config.userdata[u'redis_server']
    context.redis_port = int(context.config.userdata[u'redis_port'])
    context.solr_url = context.config.userdata[u'solr_url']
    context.UI = False

    if context.config.verbose:
        print(u'run:', context.browsertype)
    if tag == u'UI':
        context.UI = True
        if context.browsertype == u'firefox':
            use_fixture(driver.firefox_driver, context)
        elif context.browsertype == u'chrome':
            use_fixture(driver.chrome_driver, context)


def after_step(context, step):
    if step.status != u'passed':
        if context.UI:
            use_fixture(driver.screenshot, context)
