# encoding: utf-8

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from .basepage import basepage


class datasettopicpage(basepage):
    def __init__(self, context):
        context.relative_url = u'dataset/groups/' + \
                               context.datasetname
        super(datasettopicpage, self).__init__(context)
        self.topic = context.topic
    topic = u""
    locator_dictionary = {
        u'addButton':
            (By.XPATH,
             u'//button[contains(text(), "Add to topic")]'),
        u'topicsInput':
            (By.XPATH,
             u'//div[contains(@id, "field-add_group")]/label/following-sibling::input'),
        u'topicsField':
            (By.ID, u'field-add_group'),
        u'topicsOptions':
            (By.XPATH, u'//select[@id="field-add_group"]/option'),
        u'topicsRemoveButton':
            (By.XPATH, u'//input[contains(@title, "Remove dataset from this topic")]')
        }

    def check_autocomplete(self, word):
        found = False
        try:
            self.driver.find_element_by_xpath(
                u'//ul/li/div[@role="option" and contains(text(),"{}")]'.format(word))
            found = True
        except NoSuchElementException:
            found = False
        return found

    def choose_autocomplete(self, word):
        found = self.check_autocomplete(word)
        if found:
            self.driver.find_element_by_xpath\
                (u'//ul/li/div[@role="option" and contains(text(),"{}")]'.format(word)).click()

    def associate_topic(self, topic):
        super(datasettopicpage, self).fill_field(
            self.topicsInput, topic, False)
        assert self.check_autocomplete(topic)
        self.choose_autocomplete(topic)
        self.addButton.click()

    def remove_topic(self, topic):
        target_element = self.driver.find_element_by_xpath(u'//a[contains(@title, "{}")]'.format(topic))
        hover = ActionChains(self.driver).move_to_element(target_element)
        hover.perform()
        self.topicsRemoveButton.click()


