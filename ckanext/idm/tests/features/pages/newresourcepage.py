from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .basepage import basepage


class newresourcepage(basepage):

    def __init__(self, context):
        context.relative_url = u'dataset/{}/resource/new'.format(context.datasetname)
        super(newresourcepage, self).__init__(context)

    locator_dictionary = {
        u'uploadTab': (By.ID, u'field-image-upload'),
        u'linkTab': (By.PARTIAL_LINK_TEXT, u'Link'),
        u'urlField': (By.ID, u'field-image-url'),
        u'nameField': (By.ID, u'field-name'),
        u'purposeField': (By.ID, u'field-purpose'),
        u'descriptionField': (By.ID, u'field-description'),
        u'formatField': (By.ID, u'field-purpose'),
        u'previousButton': (By.XPATH, u'//button[contains(text(),"Previous")]'),
        u'saveButton':
            (By.XPATH, u'//button[contains(text(),"Save & add another")]'),
        u'finishButton': (By.XPATH, u'//button[contains(text(),"Finish")]'),
        u'addButton' : (By.XPATH, u'//button[contains(text(),"Add")]'),
        u'manageDatasetTab': (By.PARTIAL_LINK_TEXT, u'Manage'),
        u'viewDatasetTab': (By.PARTIAL_LINK_TEXT, u'View dataset')
    }

    def fill_required(self, fieldname, fieldtext):
        required_fields = {
            u'URL': self.urlField,
            u'Name': self.nameField,
            u'Type': self.purposeField
        }
        if fieldname in required_fields.keys():
            self.fill_field(required_fields[fieldname],
                            fieldtext, fieldname)
        else:
            raise Exception(u'field not in the required list:', fieldname)

    def fill_optional(self, fieldname, fieldtext):
        optional_fields = {
            u'Description': self.descriptionField,
            u'Format': self.formatField
        }
        if fieldname in optional_fields.keys():
            self.fill_field(optional_fields[fieldname],
                            fieldtext, fieldname)
        else:
            raise Exception(u'field not in the optional list:', fieldname)

    def fill_field(self, fieldname, fieldtext, handler=None, autocomplete=False):
        if handler in ['Format']:
            if not autocomplete:
                self.driver.find_element_by_xpath(
                    u'//div//label[contains(text(),"{}")]/following-sibling::input'.format(handler)) \
                    .send_keys(fieldtext, Keys.RETURN)
            else:
                self.driver.find_element_by_xpath(
                    u'//div//label[contains(text(),"{}")]/following-sibling::input'.format(handler)) \
                    .send_keys(fieldtext, Keys.DOWN)
        else:
            super(newresourcepage, self).fill_field(fieldname, fieldtext)
