from selenium.webdriver.common.by import By
from .basepage import basepage


class newresourcepage(basepage):

    def __init__(self, context):
        context.relative_url = u'dataset/' + context.resourcename + u'/resource'
        super().__init__(context)
