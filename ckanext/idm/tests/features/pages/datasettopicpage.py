from selenium.webdriver.common.by import By
from .basepage import basepage

class datasettopicpage(basepage):
    def __init__(self, context):
        context.relative_url = u'dataset/groups/' + \
                               context.datasetname
        super(datasettopicpage, self).__init__(context)
        self.topic = context.topic
    topic = u""
    locator_dictionary = {
        u'addButton': (By.XPATH, u'//button[contains(text(), "Add to topic")]'),
        u'topicsInput': (By.XPATH, u'//div[contains(@id, "field-add_group")]/label/following-sibling::input'),
        u'topicsField': (By.ID, u'field-add_group'),
        u'topicsOptions': (By.XPATH, u'//select[@id="field-add_group"]/option')
        }

    def check_autocomplete(self, word):
        found = False
        try:
            self.driver.find_element_by_xpath(u'//ul/li/div[@role="option" and contains(text(),"{}")]'.format(word))
            found = True
        except NoSuchElementException:
            found = False
        return found

    def choose_autocomplete(self, word):
        found = self.check_autocomplete(word)
        if found:
            self.driver.find_element_by_xpath\
                (u'//ul/li/div[@role="option" and contains(text(),"{}")]'.format(word)).click()
