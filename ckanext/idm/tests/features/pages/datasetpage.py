# encoding: utf-8

from selenium.webdriver.common.by import By
from .basepage import basepage


class datasetpage(basepage):
    def __init__(self, context):
        try:
            datasetname = context.datasetname
        except AttributeError:
            datasetname = u''
        context.relative_url = u'dataset' + u'/{}'.format(datasetname)\
            if datasetname != u'' else u'dataset'
        super(datasetpage, self).__init__(context)

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
        u'resourceItems': (By.CSS_SELECTOR, u'li.resource-item'),
        u'topicLink': (By.XPATH,
                       u'//div[@role="main"]//a[contains(text(),"Topics")]'),
        u'manageLink': (By.XPATH,
                        u'//a[contains(@href,"/dataset/edit/")]'),
        u'metadataRows': (By.XPATH, u'//table//tr'),
        u'titleElem': (By.CSS_SELECTOR,
                       u'div.module-content h1.heading'),
        u'descriptionElem': (By.CSS_SELECTOR, u'div.notes p'),

        # not found
        u'notfoundElem': (By.XPATH,
                          u'//div[contains(text(),"Dataset not found")]')
    }

    def find_resource_by_title(self, title):
        resourcefound = False
        for resource in self.resourceItems:
            link = resource.find_element_by_tag_name(u'a')
            if str(link.text).strip(u' ') == title:
                linkref = link.get_attribute(u'href')
                resourceid = linkref.split(u'/')[-1]
                resourcefound = True
                return resourceid
        if not resourcefound:
            raise Exception(u'resource not found:', title)

    def check_metadata(self, field, value):
        metadatafound = False
        if field == u'Description':
            description = self.descriptionElem.text
            metadatafound = True if description.strip() == value else False
        elif field == u'Title':
            title = self.titleElem.text
            metadatafound = True if title.strip() == value else False
        else:
            for row in self.metadataRows:
                key = row.find_element_by_tag_name(u'th').text
                key = u'Maintainer email' \
                    if key == u'Maintainer'else key
                key = u'Spatial Extent' \
                    if key == u'Extent' else key
                if key.strip() == field:
                    print(u"Field: {}".format(key))
                    if key == u'Maintainer email':
                        actual_value = row.find_element_by_xpath(u'.//td/a').text
                    elif key == u'Restricted':
                        actual_value = u'False' \
                            if row.find_element_by_tag_name(u'td').text.strip() == u'' \
                            else u'True'
                    else:
                        actual_value = row.find_element_by_tag_name(u'td').text
                    print(u"Value: {}".format(actual_value))
                    if value.strip() == actual_value.strip():
                        metadatafound = True

                    break
        if not metadatafound:
            raise Exception(u'value "{}" does not match {}:'.format(field, value))
