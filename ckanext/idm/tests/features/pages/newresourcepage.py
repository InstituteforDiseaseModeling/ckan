from selenium.webdriver.common.by import By
from .basepage import basepage

class newresourcepage(basepage):

    def __init__(self, context):
        context.relative_url="dataset/new_resource/" + context.datasetname
        super().__init__(context)

    locator_dictionary = {
        "uploadTab" : (By.ID, 'field-image-upload'),
        "linkTab" : (By.PARTIAL_LINK_TEXT, 'Link'),
        "urlField": (By.ID, 'field-image-url'),
        "nameField" : (By.ID, 'field-name'),
        "descriptionField" : (By.ID, 'field-description'),
        "previousButton" : (By.XPATH, '//button[contains(text(),"Previous"]'),
        "saveButton": (By.XPATH, '//button[contains(text(),"Save & add another"]'),
        "finishButton": (By.XPATH, '//button[contains(text(),"Finish")]'),
        "manageDatasetTab" : (By.PARTIAL_LINK_TEXT, 'Manage'),
        "viewDatasetTab" : (By.PARTIAL_LINK_TEXT, 'View dataset')
    }
