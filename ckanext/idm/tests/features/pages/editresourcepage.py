# encoding: utf-8

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .newresourcepage import newresourcepage


class editresourcepage(newresourcepage):
    def __init__(self, context):
        datasetname = context.datasetname
        context.relative_url = u'/dataset/{}/resource/'.format(datasetname)
        if hasattr(context, 'resourcename'):
            context.relative_url = context.relative_url + context.resourcename
        super(editresourcepage, self).__init__(context)

    locator_dictionary = {
        u'uploadTab': (By.ID, u'field-image-upload'),
        u'linkTab': (By.PARTIAL_LINK_TEXT, u'Link'),
        u'urlField': (By.ID, u'field-image-url'),
        u'nameField': (By.ID, u'field-name'),
        u'purposeField': (By.ID, u'field-purpose'),
        u'descriptionField': (By.ID, u'field-description'),
        u'formatField': (By.ID, u'field-purpose'),
        u'previousButton': (By.XPATH, u'//button[contains(text(),"Previous")]'),
        u'updateButton': (By.XPATH, u'//button[contains(text(),"Update Resource")]'),
        u'deleteLink': (By.PARTIAL_LINK_TEXT, u'Delete'),
        u'deleteConfirmButton': (By.XPATH, u'//button[contains(text(),"Confirm")]'),
        u'deleteCancelButton': (By.XPATH, u'//button[contains(text(),"Cancel)]'),
        u'finishButton': (By.XPATH, u'//button[contains(text(),"Finish")]'),
        u'manageDatasetTab': (By.PARTIAL_LINK_TEXT, u'Manage'),
        u'viewDatasetTab': (By.PARTIAL_LINK_TEXT, u'View dataset')
     }

    def delete(self):
        self.deleteLink.click()
        wait = WebDriverWait(self.driver, 10)
        elem = wait.until(EC.element_to_be_clickable((By.XPATH, u'//button[contains(text(),"Confirm")]')))
        elem.click()

    def edit(self, fieldname, fieldvalue):
        fields = {
            u'URL': self.urlField,
            u'Name': self.nameField,
            u'Type': self.purposeField,
            u'Description': self.descriptionField,
            u'Format': self.formatField
        }
        if fieldname in fields.keys():
            super(editresourcepage, self).fill_field(fields[fieldname], fieldvalue, fieldname)
