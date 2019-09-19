# encoding: utf-8

from selenium.webdriver.common.by import By
from .basepage import basepage


class homepage(basepage):

    def __init__(self, context):
        super(homepage, self).__init__(context)

    locator_dictionary = {
        u'logo': (By.CSS_SELECTOR, u'a.logo'),
        u'datasetTab': (By.PARTIAL_LINK_TEXT, u'Datasets'),
        u'organizationTab': (By.PARTIAL_LINK_TEXT, u'Organizations'),
        u'groupTab': (By.PARTIAL_LINK_TEXT, u'Group'),
        u'aboutTab': (By.PARTIAL_LINK_TEXT, u'About'),
        u'loginTab': (By.PARTIAL_LINK_TEXT, u'Log in'),
        u'loggedinText': (By.CSS_SELECTOR, u'span.username'),
        u'registerTab': (By.PARTIAL_LINK_TEXT, u'Register'),
        u'searchTextField': (By.ID, u'field-sitewide-search'),
        u'searchButton': (By.CSS_SELECTOR, u'button.btn-search'),
        u'searchDatasetField' : (By.ID, u'field-giant-search')
    }
