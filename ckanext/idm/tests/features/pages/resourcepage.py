# encoding: utf-8

from selenium.webdriver.common.by import By
from .basepage import basepage
import requests


class resourcepage(basepage):

    def __init__(self, context):
        context.relative_url = u'dataset/' + \
                               context.datasetname + \
                               u'/resource/' + \
                               context.resourcename
        super(resourcepage, self).__init__(context)

    locator_dictionary = {
        u'metadataRows': (By.XPATH, u'//table//tr')
    }

    def check_metadata(self, field, value):
        metadatafound = False
        if field == u'Name':
            actual_value = self.driver.find_element_by_xpath(
                u'//h1[@class="page-heading"]').text
            metadatafound = True \
                if actual_value.strip() == value else False
        elif field == u'Description':
            actual_value = \
                self.driver.find_element_by_css_selector(
                    u'div.notes p').text
            metadatafound = True \
                if actual_value.strip() == value else False
        for row in self.metadataRows:
            key = row.find_element_by_tag_name(u'th').text
            key = u'Type' if key == u'Purpose' else key
            if key.strip() == field:
                print(u"Field: {}".format(key))
                if key == u'License':
                    actual_value = \
                        row.find_element_by_xpath(u'.//td/a').text
                else:
                    actual_value = \
                        row.find_element_by_tag_name(u'td').text
                print(u"Value: {}".format(actual_value))
                if key == u'Format' and value.strip().lower() in actual_value.strip().lower():
                    metadatafound = True
                elif value.strip() == actual_value.strip():
                    metadatafound = True
                break
        if not metadatafound:
            raise Exception(u'value "{}" does not match {}:'.format(field, value))

    def check_download_resource(self, filename):
        downloadlink = self.driver.find_element_by_xpath(u'//a[contains(@href,"{}")]'.format(filename)).get_attribute(u"href")
        ret = request = requests.get(downloadlink)
        assert ret.status_code == 200
