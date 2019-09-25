# encoding: utf-8
from selenium.webdriver.common.by import By
from behave import step, given, when, then
from pages.datasetpage import datasetpage
from pages.resourcepage import resourcepage
from pages.homepage import homepage
import datetime

@step(u'I am on resource page')
def step_impl(context):
    context.resourcepage= resourcepage(context)
    context.resourcepage.visit()


@step(u'I can Click download and save a copy successfully')
def step_impl(context):
    filename = context.testfile.split('/')[-1]
    context.resourcepage.check_download_resource(filename)


@step(u'the dataset is created with metadata {filter}={value}')
def step_impl(context, filter, value):
    context.testtable = [
        {u'fields': u'Title', u'values': u'test_updateDataset' + u" " + datetime.datetime.now().strftime(u"%y%m%d_%H%M%S")},
        {u'fields': u'Description', u'values': u'This is a test'},
        {u'fields': u'Maintainer_email', u'values': u'test@idmod.org'},
        {u'fields': u'Purpose', u'values': u'Raw Data'},
        {u'fields': u'Research_Group', u'values': u'Test Automation'},
        {u'fields': u'Disease', u'values': u'Any'},
        {u'fields': u'Start_Date', u'values': u'1977-01-01'},
        {u'fields': u'End_Date', u'values': u'2019-03-01'},
        {u'fields': u'Location', u'values': u'World'},
        {u'fields': u'Publisher', u'values': u'IDM'},
        {u'fields': u'Acquisition_Date', u'values': u'2019-03-01'},
        {u'fields': u'Version', u'values': u'1.0'},
        {u'fields': u'Visibility', u'values': u'Public'},
        {u'fields': u'Restricted', u'values': u'False'},
        {u'fields': u'License', u'values': u'Creative Commons Attribution'}
    ]
    for row in context.testtable:
        if row[u"fields"] == filter:
            row[u'values'] = value

    context.execute_steps(u'''
    Given I have created a dataset with resource (tag:addDataRequiredFields)
    ''')

