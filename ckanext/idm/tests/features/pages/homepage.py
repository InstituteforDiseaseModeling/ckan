from selenium.webdriver.common.by import By
from .basepage import basepage

class homepage(basepage):

    def __init__(self, context):
        super().__init__(context)

    locator_dictionary = {
        "logo": (By.CSS_SELECTOR, 'a.logo'),
        "datasetTab" : (By.PARTIAL_LINK_TEXT, 'Datasets'),
        "organizationTab": (By.PARTIAL_LINK_TEXT, 'Organizations'),
        "groupTab": (By.PARTIAL_LINK_TEXT, 'Group'),
        "aboutTab": (By.PARTIAL_LINK_TEXT, 'About'),
        "loginTab": (By.PARTIAL_LINK_TEXT, 'Log in'),
        "loggedinText" :(By.CSS_SELECTOR, 'span.username'),
        "registerTab" : (By.PARTIAL_LINK_TEXT, 'Register'),
        "searchTextField" : (By.ID, 'field-sitewide-search'),
        "searchButton" : (By.CSS_SELECTOR, 'button.btn-search')
    }
