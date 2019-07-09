from selenium.webdriver.common.by import By
from .basepage import basepage

class datasetpage(basepage):

    def __init__(self, context):
        try:
            datasetname = context.datasetname
        except:
            datasetname=''
        context.relative_url="dataset"+ "/{}".format(datasetname) if datasetname != '' else "dataset"
        super().__init__(context)

    locator_dictionary = {
        "searchTextField" : (By.ID, 'field-giant-search'),
        "searchButton" : (By.CSS_SELECTOR, 'span.input-group-btn'),
        "datasetItems" : (By.CSS_SELECTOR, 'li.dataset-item'),
        "adddataTab": (By.PARTIAL_LINK_TEXT, 'Add Dataset'),

        #found dataset
        "exploreResourceTab": (By.PARTIAL_LINK_TEXT, 'Explore'),
        "moreinfoTab": (By.PARTIAL_LINK_TEXT, 'More information'),
        "gotoReourceTab": (By.PARTIAL_LINK_TEXT, 'Go to resource'),
        "editResourceTab": (By.PARTIAL_LINK_TEXT, 'Edit'),
        "resourceItems" : (By.CSS_SELECTOR, 'li.resource-item')
    }

    def findResourceByTitle(self, title):
        resourceFound = False
        for resource in self.resourceItems:
            link = resource.find_element_by_tag_name('a')
            if str(link.text).strip(' ')==title:
                linkref = link.get_attribute("href")
                resourceid = linkref.split('/')[-1]
                resourceFound = True
                return resourceid
        if not resourceFound:
            raise Exception("resource not found:", title)

