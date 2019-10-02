# encoding: utf-8

import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from behave import step, given, when, then
from pages.datasetpage import datasetpage
from pages.editdatasetpage import editdatasetpage
from pages.resourcepage import resourcepage
from pages.newresourcepage import newresourcepage
from pages.editresourcepage import editresourcepage
from pages.datasettopicpage import datasettopicpage


@step(u'I have a dataset created with {data_values} for {data_fields}')
def step_impl(context, data_fields, data_values):
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
        if row[u"fields"] == data_fields:
            row[u'values'] = data_values

    context.execute_steps(u'''
    Given I have created a dataset with resource (tag:addDataRequiredFields)
    ''')


@step(u'I am on dataset page')
def step_impl(context):
    context.datasetpage = datasetpage(context)

    
@step(u'I click Manage')
def step_impl(context):
    context.datasetpage.manageLink.click()
    context.editdatasetpage = editdatasetpage(context)
    

@step(u'I enter {new_values} in {data_fields} to update dataset and expect changes to be there')
def step_impl(context, new_values, data_fields):
    if data_fields == u'Spatial Extent':
        context.editdatasetpage.fill_optional(u'spatial Mode', u'True')
    if data_fields in [u'Quality Issues',
                       u'Quality Rating',
                       u'Spatial Gaps',
                       u'Temporal Gaps',
                       u'Spatial Extent',
                       u'Country'
                       ]:
        context.editdatasetpage.fill_optional(data_fields, new_values)
    else:
        context.editdatasetpage.fill_required(data_fields, new_values)
    context.editdatasetpage.updateDatasetButton.click()
    context.datasetpage = datasetpage(context)
    context.datasetpage.visit()
    if data_fields not in [u'Visibility', u'License']:
        context.datasetpage.check_metadata(data_fields, new_values)


@step(u'I can delete the dataset')
def step_impl(context):
    context.editdatasetpage = editdatasetpage(context)
    context.editdatasetpage.delete()
    context.datasetpage = datasetpage(context)
    context.datasetpage.visit()
    context.datasetpage.check_metadata(u'State', u'deleted')


@step(u'I go the Edit Resource tab')
def step_impl(context):
    context.editdatasetpage.editResourceLink.click()
    if context.editdatasetpage.resourceElems is list:
        context.resourcename = context.editdatasetpage.resourceElems[0].get_attribute(u'href').split(u'/')[-1]
        context.editdatasetpage.resourceElems[0].click()
    else:
        context.resourcename = context.editdatasetpage.resourceElems.get_attribute(u'href').split(u'/')[-2]
        context.editdatasetpage.resourceElems.click()


@step(u'I can delete the resource')
def step_impl(context):
    context.editresourcepage = editresourcepage(context)
    context.editresourcepage.delete()
    context.resourcepage = resourcepage(context)
    context.resourcepage.visit()
    assert u'404' in context.resourcepage.driver.title


@step(u'I go the Add Resource tab')
def step_impl(context):
    context.editdatasetpage.editResourceLink.click()
    context.editdatasetpage.addResourceLink.click()
    context.newresourcepage = newresourcepage(context)


@step(u'I add a new resource')
def step_impl(context):
    context.added_resource_name = u'ThisIsNewlyAdded'
    context.newresourcepage.fill_required(u'Name', context.added_resource_name)
    context.newresourcepage.finishButton.click()


@step(u'I should see both old and new resources')
def step_impl(context):
    context.datasetpage = datasetpage(context)
    context.datasetpage.visit()
    context.datasetpage.find_resource_by_title(context.added_resource_name)


@step(u'I change {new_value} for {field}')
def step_impl(context, new_value, field):
    context.editresourcepage = editresourcepage(context)
    context.editresourcepage.edit(field, new_value)


@step(u'I click update resource')
def step_impl(context):
    context.editresourcepage.updateButton.click()


@step(u'I should see the {new_value} appears for {field}')
def step_impl(context, new_value, field):
    context.resourcepage = resourcepage(context)
    context.resourcepage.check_metadata(field, new_value)


@step(u'the dataset is created and associated with a topic Mortality')
def step_impl(context):
    context.topic = u'Mortality'
    context.execute_steps(u'''
       Given I have created a dataset with resource (tag:addDataRequiredFields)
       When I click on the Topic tab on dataset page
       ''')
    context.datasettopicpage = datasettopicpage(context)
    context.datasettopicpage.associate_topic(context.topic)


@step(u'I can change the topic association to Births from the topic tab')
def step_impl(context):
    context.datasettopicpage = datasettopicpage(context)
    context.datasettopicpage.remove_topic(context.topic)
    context.datasettopicpage.associate_topic(u"Births")
    assert len(
        context.datasettopicpage.driver.find_elements_by_xpath(
            u'//a//span[contains(text(),"Births")]')) == 1
