import uuid
import datetime
import time
import os
from selenium.webdriver.common.keys import Keys
from behave import step, given, when, then
from pages.loginpage import loginpage
from pages.homepage import homepage
from pages.datasetpage import datasetpage
from pages.newdatasetpage import newdatasetpage
from pages.newresourcepage import newresourcepage
from pages.dashboardpage import dashboardpage
from pages.datasettopicpage import datasettopicpage



@step(u'I am registered')
def step_impl(context):
    try:
        context.execute_steps(u'When I am logged in')
        pass
    except RuntimeError:
        raise RuntimeError(u'User not registered!')


@step(u'I am logged in')
def step_impl(context):
    context.timeout = 5
    context.homepage = homepage(context)
    context.homepage.visit()
    loggedin = False
    repeat = 3
    i = 0
    while not loggedin and i < repeat:
        try:
            context.homepage.visit()
            loggedin = context.homepage.loggedinText
            if loggedin is None:
                raise RuntimeError(u"not yet login")
            i = + 1
        except RuntimeError:
            loggedin = False
            context.loginpage = loginpage(context)
            context.loginpage.visit()
            context.loginpage.login(context.ckan_user, context.ckan_password)

    if not loggedin:
        raise Exception(u"login failed")


@step(u'I am added to the research group as editor')
def step_impl(context):
    context.execute_steps(u'When I am logged in')
    context.dashboardpage = dashboardpage(context)
    context.dashboardpage.visit()
    context.dashboardpage.myResearchLink.click()
    myResearchList = context.dashboardpage.myResearchList

    for row in context.table:
        added = False
        for item in myResearchList:
            if row[u'Research Group'] in item.get_attribute(u'title'):
                added = True
        assert added, u'user not added to {}'.format(row[u'Research Group'])

           
@step(u'a list of pre-defined "Tags" has been loaded in the system')
def step_impl(context):
    for row in context.table:
        print(u'Please make sure to create the tags: {}'.format(row[u'Tags']))
    pass


@step(u'a list of pre-defined "Topics" has been loaded in the system')
def step_impl(context):
    for row in context.table:
        print(u'Please make sure to create the topics: {}'.format(row[u'Topic']))
    pass


@step(u'I have the file')
def step_impl(context):
    context.testfile = u'testfiles/test.png'


@step(u'I have dataset info')
def step_impl(context):
    if not hasattr(context, 'testtable'):
        context.testtable = [
            {u'fields': u'Title', u'values': u'test_addDataset' + datetime.datetime.now().strftime(u"%y%m%d_%H%M%S")},
            {u'fields': u'Description', u'values': u'This is a test'},
            {u'fields': u'Maintainer_email', u'values': u'test@idmod.org'},
            {u'fields': u'Purpose', u'values': u'Raw Data'},
            {u'fields': u'Research_Group', u'values': u'Test Automation'},
            {u'fields': u'Disease', u'values': u'Any'},
            {u'fields': u'Start_Date', u'values': u'2018-01-01'},
            {u'fields': u'End_Date', u'values': u'2019-03-01'},
            {u'fields': u'Location', u'values': u'World'},
            {u'fields': u'Publisher', u'values': u'IDM'},
            {u'fields': u'Acquisition_Date', u'values': u'2019-03-01'},
            {u'fields': u'Version', u'values': u'1.0'},
            {u'fields': u'Visibility', u'values': u'Public'},
            {u'fields': u'Restricted', u'values': u'False'},
            {u'fields': u'License', u'values': u'Creative Commons Attribution'}
        ]



@step(u'I click "Add Dataset"')
def step_impl(context):
    context.datasetpage = datasetpage(context)
    context.datasetpage.visit()
    context.datasetpage.adddataTab.click()


@step(u'I am redirected to the Create Dataset page')
def step_impl(context):
    assert context.datasetpage
    context.newdatasetpage = newdatasetpage(context)
    context.newdatasetpage.visit()


@step(u'I am ready to create dataset (tag:addDataset)')
def step_impl(context):
    context.execute_steps(u'''
    Given I have the file
    Given I have dataset info
    When I click "Add Dataset"
    Then I am redirected to the Create Dataset page
    ''')


@step(u'I must set all required dataset fields')
def step_impl(context):
    if context.table is not None:
        context.testtable = context.table
    for row in context.testtable:
        context.newdatasetpage.fill_required(row[u"fields"].replace(u'_',u' '), row[u"values"])


@step(u'I must set required dataset fields')
def step_impl(context):
    for row in context.table:
        context.newdatasetpage.fill_required(row[u"fields"], row[u"values"])


@step(u'I must set required Purpose to {purpose}')
def step_impl(context, purpose):
    purpose = u"Raw Data" if purpose == u"<purpose>" else purpose
    context.newdatasetpage.fill_required(u'Purpose', purpose)
    

@step(u'I must set required Disease to {disease}')
def step_impl(context, disease):
    disease = u"Any" if disease == u"<disease>" else disease
    context.newdatasetpage.fill_required(u'Disease', disease)


@step(u'I must set required Location to {location}')
def step_impl(context, location):
    location = u"World" if location == u"<location>" else location
    context.newdatasetpage.fill_required(u'Location', location)


@step(u'I must set required Visibility to {visibility}')
def step_impl(context, visibility):
    visibility = u"Public" if visibility == u"<visibility>" else visibility
    context.newdatasetpage.fill_required(u'Visibility', visibility)


@step(u'I must set required Restricted to {restricted}')
def step_impl(context, restricted):
    restricted = u"False" if restricted == u"<restricted>" else restricted
    context.newdatasetpage.fill_required(u'Restricted', restricted)


@step(u'I must set required Publisher to {publisher}')
def step_impl(context, publisher):
    publisher = u"IDM" if publisher == u"<publisher>" else publisher
    context.newdatasetpage.fill_required(u'Publisher', publisher)


@step(u'I have filled in all required fields(tag:allRequiredFields)')
def step_impl(context):
    context.execute_steps(u'''
    Given I am ready to create dataset (tag:addDataset)
    Then I must set all required dataset fields
    ''')
    context.newdatasetpage = newdatasetpage(context)


@step(u'I set all optional dataset fields')
def step_impl(context):
    for row in context.table:
        context.newdatasetpage.fill_optional(row[u"fields"], row[u"values"])


@step(u'I can click "Add Data"')
def step_impl(context):
    context.datasetname = str(uuid.uuid4())
    context.newdatasetpage.set_url(context.datasetname)
    context.newdatasetpage.addDataButton.click()
    context.newresourcepage = newresourcepage(context)
    assert context.newresourcepage.nameField.is_displayed()


@step(u'I start to type a tag that is a pre-defined {tags}')
def step_impl(context, tags):
    prefix = str(tags)[:1]
    context.newdatasetpage.fill_field(
        context.newdatasetpage.tagsField, prefix, u'Tags', True)
    time.sleep(1)


@step(u'The system suggests the existing tag:{tags}')
def step_impl(context, tags):
    assert context.newdatasetpage.check_autocomplete(tags)


@step(u'I can select the pre-existing {tags} to auto-complete the tag')
def step_impl(context, tags):
    context.newdatasetpage.choose_autocomplete(tags)


@step(u'I fill out the Spatial section for {location}')
def step_impl(context, location):
    prefix = str(location)
    context.newdatasetpage.fill_field(
        context.newdatasetpage.locationField, prefix, u'Location', True)
    time.sleep(1)


@step(u'I will see an optional field {location_dot_name} to enter text')
def step_impl(context, location_dot_name):
    assert context.newdatasetpage.check_autocomplete(location_dot_name)


@step(u'I can click "Link"')
def step_impl(context):
    context.newresourcepage = newresourcepage(context)
    context.newresourcepage.visit()
    context.newresourcepage.linkTab.click()


@step(u'I must set required resource fields')
def step_impl(context):
    if context.table is not None:
        context.resourcetable = context.table
    for row in context.resourcetable:
        context.newresourcepage.fill_required(row['fields'], row['values'])


@step(u'I can set optional resource fields')
def step_impl(context):
    for row in context.table:
        context.newresourcepage.fill_optional(row['fields'], row['values'])


@step(u'I can click "Save & add another"')
def step_impl(context):
    context.newresourcepage.saveButton.click()


@step(u'I can click "Finish"')
def step_impl(context):
    context.newresourcepage.finishButton.click()


@step(u'I can click "Upload" and select a local file')
def step_impl(context):
    filename = os.path.abspath(context.testfile)
    context.newresourcepage.uploadTab.send_keys(filename)


@step(u'I can set required "Type" {type}')
def step_impl(context, type):
    context.newresourcepage.fill_required(u'Type', type)


@step(u'I have created a dataset with resource (tag:addDataRequiredFields)')
def step_impl(context):
    context.resourcetable = [
        {u'fields': u'Name', u'values': u'test data'},
        {u'fields': u'URL', u'values': u'http://google.com'},
        {u'fields': u'Type', u'values': u'Data'}]
    context.execute_steps(u'''
        Given I have filled in all required fields(tag:allRequiredFields)
        When I can click "Add Data"
        And I can click "Link"
        And I must set required resource fields
        And I can click "Finish"
        ''')


@step(u'I click on the Topic tab on dataset page')
def step_impl(context):
    context.datasetpage = datasetpage(context)
    context.datasetpage.topicLink.click()


@step(u'A drop-down of available {topic} are listed')
def step_impl(context, topic):
    foundTopic = False
    context.topic = topic
    context.datasettopicpage = datasettopicpage(context)
    assert len(context.datasettopicpage.topicsOptions) > 1
    context.datasettopicpage.fill_field(context.datasettopicpage.topicsInput, u" ", False)
    for option in context.datasettopicpage.topicsOptions:
        if topic in option.get_attribute(u'text'):
            foundTopic = True
            break
    assert foundTopic
    context.datasettopicpage.choose_autocomplete(topic)
            

@step(u'I can select the pre-existing {topic} to auto-complete their topic field')
def step_impl(context, topic):
    context.topic = topic
    prefix = str(topic)[:1]
    context.datasettopicpage.fill_field(context.datasettopicpage.topicsInput, prefix, False)
    assert context.datasettopicpage.check_autocomplete(topic)
    context.datasettopicpage.choose_autocomplete(topic)
    context.datasettopicpage.addButton.click()
    assert len(
        context.datasettopicpage.driver.find_elements_by_xpath(u'//a//span[contains(text(),"{}")]'.format(topic))) == 1
