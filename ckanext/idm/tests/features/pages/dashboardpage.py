# encoding: utf-8

from selenium.webdriver.common.by import By
from .basepage import basepage


class dashboardpage(basepage):

    def __init__(self, context):
        context.relative_url = u'/dashboard'
        super(dashboardpage, self).__init__(context)

    locator_dictionary = {
        u'myNewFeedLink': (By.LINK_TEXT, u'News feed'),
        u'myDatasetLink': (By.LINK_TEXT, u'My Datasets'),
        u'myResearchLink': (By.LINK_TEXT, u'My Research Groups'),
        u'myTopicsLink': (By.LINK_TEXT, u'My Topics'),
        u'myResearchList': (By.XPATH, u'//a[contains(@href,"/organization/")]')
    }
