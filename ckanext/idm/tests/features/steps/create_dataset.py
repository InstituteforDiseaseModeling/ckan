import uuid
from behave import *
from utilities import db
from pages.loginpage import loginpage
from pages.homepage import homepage
from pages.datasetpage import datasetpage
from pages.newdatasetpage import newdatasetpage
from pages.newresourcepage import newresourcepage

@step("The use has registered")
def user_registered(context):
    record = db.get_record(context, "SELECT name from public.""user"" where name = '{}'".format(context.ckan_user))
    if record is None or len(record) != 1:
        raise Exception("User not registered:", context.ckan_user)

@step("The user is logged in")
def ensure_login(context):
    context.timeout=5
    context.homepage = homepage(context)
    context.homepage.visit()
    loggedin = False
    repeat = 3
    i = 0
    while not loggedin and i < repeat:
        try:
            context.homepage.visit()
            loggedin = context.homepage.loggedinText
            i =+1
        except:
            loggedin = False
            context.loginpage = loginpage(context)
            context.loginpage.visit()
            context.loginpage.login(context.ckan_user, context.ckan_password)

@step("The user is added to the organization")
def ensure_in_org(context):
    pass

@step("I have a link for a dataset")
def get_dataset_link(context):
    for row in context.table:
        context.linkname = row["name"]
        context.linkurl =row["url"]
        context.linkdescription = row["description"]

@step("I click \"new dataset\"")
def get_dataset_page(context):
    context.homepage.datasetTab.click()
    context.datasetpage = datasetpage(context)
    context.datasetpage.adddataTab.click()
    context.newdatasetpage = newdatasetpage(context)

@step("I am required to fill values in these fields")
def fill_required_fields(context):
    for row in context.table:
        context.newdatasetpage.fillRequired(row["fields"], row["values"])
    context.datasetname = str(uuid.uuid4())
    context.newdatasetpage.editButton.click()
    context.newdatasetpage.urlnameField.clear()
    context.newdatasetpage.urlnameField.send_keys(context.datasetname)

@step("I can optionally add up to 3 fields with values")
def fill_custom_fields(context):
    fieldDict ={}
    for row in context.table:
        fieldDict[row["fields"]] = row["values"]
    context.newdatasetpage.fillCustom(fieldDict)

@step("I can click add data and enter name, description  and url of the third party source")
def add_resource(context):
    context.newdatasetpage.addDataButton.click()
    context.newresourcepage = newresourcepage(context)
    context.newresourcepage.linkTab.click()
    context.newresourcepage.urlField.send_keys(context.linkurl)
    context.newresourcepage.nameField.send_keys(context.linkname)
    context.newresourcepage.descriptionField.send_keys(context.linkdescription)
    context.newresourcepage.finishButton.click()

