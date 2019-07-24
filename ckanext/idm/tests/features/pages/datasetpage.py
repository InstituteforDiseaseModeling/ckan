from selenium.webdriver.common.by import By
from .basepage import basepage


class datasetPage(basepage):
    def __init__(self, context):
        try:
            datasetname = context.datasetname
        except AttributeError:
            datasetname = ''
        context.relative_url = u'dataset' + u'/{}'.format(datasetname)\
            if datasetname != '' else u'dataset'
        super().__init__(context)

    locator_dictionary = {
        u'searchTextField': (By.ID, u'field-giant-search'),
        u'searchButton': (By.CSS_SELECTOR, u'span.input-group-btn'),
        u'datasetItems': (By.CSS_SELECTOR, u'li.dataset-item'),
        u'adddataTab': (By.PARTIAL_LINK_TEXT, u'Add Dataset'),

        # found dataset
        u'exploreResourceTab': (By.PARTIAL_LINK_TEXT, u'Explore'),
        u'moreinfoTab': (By.PARTIAL_LINK_TEXT, u'More information'),
        u'gotoReourceTab': (By.PARTIAL_LINK_TEXT, u'Go to resource'),
        u'editResourceTab': (By.PARTIAL_LINK_TEXT, u'Edit'),
        u'resourceItems': (By.CSS_SELECTOR, u'li.resource-item')
    }

    def find_resource_by_title(self, title):
        resourcefound = False
        for resource in self.resourceItems:
            link = resource.find_element_by_tag_name(u'a')
            if str(link.text).strip(' ') == title:
                linkref = link.get_attribute(u'href')
                resourceid = linkref.split('/')[-1]
                resourcefound = True
                return resourceid
        if not resourcefound:
            raise Exception(u'resource not found:', title)
