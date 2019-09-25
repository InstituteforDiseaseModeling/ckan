# encoding: utf-8

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions \
    import ElementNotInteractableException, NoSuchElementException
from .basepage import basepage


class newdatasetpage(basepage):

    def __init__(self, context):
        context.relative_url = u'dataset/new'
        super(newdatasetpage, self).__init__(context)

    locator_dictionary = {
        u'titleField': (By.ID, u'field-title'),
        u'editButton': (By.XPATH, u'//div[@class="slug-preview"]//button[contains(text(), "Edit")]'),
        u'urlnameField': (By.ID, u'field-name'),
        u'descrptionField': (By.ID, u'field-notes'),
        u'maintaineremailField': (By.ID, u'field-maintainer_email'),
        u'purposeField': (By.ID, u'field-purpose'),
        u'researchField': (By.ID, u'field-organizations'),
        u'visibilityField': (By.ID, u'field-private'),
        u'diseaseField': (By.ID, u'field-disease'),
        u'tagsField': (By.ID, u'field-tag_string'),
        u'qualityField': (By.ID, u'field-quality'),
        u'qualitynoteField': (By.ID, u'field-quality_notes'),
        u'startdateField': (By.ID, u'field-ext_startdate'),
        u'enddateField': (By.ID, u'field-ext_enddate'),
        u'temporalgapField': (By.ID, u'field-temporal_gaps'),
        u'locationField': (By.ID, u'field-location'),
        u'spatialgapField': (By.ID, u'field-spatial_gaps'),
        u'spatialField': (By.ID, u'field-spatial'),
        u'spatialResField': (By.ID, u'field-spatial_resolution'),
        u'spatialModeField': (By.ID, u'field-spatial_mode-manual'),
        u'publisherField': (By.ID, u'field-publisher'),
        u'urlField': (By.ID, u'field-url'),
        u'acquisitiondateField': (By.ID, u'field-acquisition_date'),
        u'versionField': (By.ID, u'field-version'),
        u'restrictedCheckbox': (By.ID, u'field-request_access-maintainer'),
        u'licenseField': (By.ID, u'field-license_id'),
        u'addDataButton':
            (By.XPATH, u'//button[contains(text(), "Next: Add Data")]')
    }

    def fill_required(self, fieldname, fieldtext):
        required_fields = {u'Title': self.titleField,
                           u'Description': self.descrptionField,
                           u'Maintainer email': self.maintaineremailField,
                           u'Purpose': self.purposeField,
                           u'Research Group': self.researchField,
                           u'Disease': self.diseaseField,
                           u'Start Date': self.startdateField,
                           u'End Date': self.enddateField,
                           u'Location': self.locationField,
                           u'Publisher': self.publisherField,
                           u'Acquisition Date': self.acquisitiondateField,
                           u'Version': self.versionField,
                           u'Visibility': self.visibilityField,
                           u'Restricted': self.restrictedCheckbox,
                           u'License': self.licenseField
                           }
        if fieldname in required_fields.keys():
            self.fill_field(required_fields[fieldname],
                            fieldtext, fieldname)
        else:
            raise Exception(u'field not in the required list:', fieldname)

    def fill_optional(self, fieldname, fieldtext):
        optional_fields = {
            u'Tags': self.tagsField,
            u'Quality Issues': self.qualitynoteField,
            u'Quality Rating': self.qualityField,
            u'Origin URL': self.urlField,
            u'Temporal Gaps': self.temporalgapField,
            u'Spatial Gaps': self.spatialgapField,
            u'Spatial Extent': self.spatialField,
            u'spatial Mode': self.spatialModeField
        }
        if fieldname in optional_fields.keys():
            self.fill_field(optional_fields[fieldname],
                            fieldtext, fieldname)
        else:
            raise Exception(u'field not in the optional list:', fieldname)

    def fill_field(self, fieldname, fieldtext, handler=None, autocomplete=False):
        handler = u'Maintainer' if handler == u'Maintainer email' else handler
        if handler in [u'Research Group', u'Location', u'Publisher', u'License', u'Tags', u'Maintainer']:
            if not autocomplete:
                self.driver.find_element_by_xpath(
                    u'//div//label[contains(text(),"{}")]/following-sibling::input'.format(handler))\
                    .send_keys(fieldtext, Keys.RETURN)
            else:
                self.driver.find_element_by_xpath(
                    u'//div//label[contains(text(),"{}")]/following-sibling::input'.format(handler))\
                    .send_keys(fieldtext, Keys.DOWN)
        else:
            super(newdatasetpage, self).fill_field(fieldname, fieldtext)

    def check_autocomplete(self, word):
        found = False
        try:
            self.driver.find_element_by_xpath(u'//ul/li/div[@data-value="{}" and @role="option"]'.format(word))
            found = True
        except NoSuchElementException:
            found = False
        return found

    def choose_autocomplete(self, word):
        found = self.check_autocomplete(word)
        if found:
            self.driver.find_element_by_xpath(u'//ul/li/div[@data-value="{}" and @role="option"]'.format(word)).click()

    def set_url(self, datasetname):
        try:
            self.editButton.click()
        except ElementNotInteractableException:
            print(u'Edit button is disabled but should still be able to edit URL')
        self.urlnameField.clear()
        self.urlnameField.send_keys(datasetname)
