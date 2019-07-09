from behave import *
from hamcrest import *
from pyredis import Client
from utilities import db
import pysolr
import requests

@step(u'The redis is up and running')
def step_impl(context):
    client = Client(host=context.redis_server, port=context.redis_port)
    response = client.ping()
    assert_that(response, equal_to(b'PONG'))

@step(u'The postgres database is up and running')
def step_impl(context):
    result = db.get_record(context, 'SELECT 1')
    assert_that(len(result), equal_to(1))

@step(u'The solr indexing is functioning')
def step_impl(context):
    solr = pysolr.Solr(context.solr_url, timeout=3600)
    solr.search('ckan')

@step(u'The site should be up and running')
def step_impl(context):
    r = requests.get(context.server)
    assert_that(r.status_code, 200)
