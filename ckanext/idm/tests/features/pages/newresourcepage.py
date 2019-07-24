from selenium.webdriver.common.by import By
from .basepage import basepage


class newresourcepage(basepage):

    def __init__(self, context):
        context.relative_url = u'dataset/new_resource/' + context.datasetname
        super().__init__(context)

    locator_dictionary = {
        u'uploadTab': (By.ID, u'field-image-upload'),
        u'linkTab': (By.PARTIAL_LINK_TEXT, u'Link'),
        u'urlField': (By.ID, u'field-image-url'),
        u'nameField': (By.ID, u'field-name'),
        u'descriptionField': (By.ID, u'field-description'),
        u'previousButton': (By.XPATH, u'//button[contains(text(),"Previous"]'),
        u'saveButton':
            (By.XPATH, u'//button[contains(text(),"Save & add another"]'),
        u'finishButton': (By.XPATH, u'//button[contains(text(),"Finish")]'),
        u'manageDatasetTab': (By.PARTIAL_LINK_TEXT, u'Manage'),
        u'viewDatasetTab': (By.PARTIAL_LINK_TEXT, u'View dataset')
    }
