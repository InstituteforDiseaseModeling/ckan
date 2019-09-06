from selenium.webdriver.common.by import By
from .basepage import basepage


class resourcepage(basepage):

    def __init__(self, context):
        context.relative_url = u'dataset/' + \
                               context.datasetname + \
                               u'/resource' + \
                               context.resourcename
        super(resourcepage, self).__init__(context)
