# encoding: utf-8

from datetime import datetime
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, \
    StaleElementReferenceException, \
    NoSuchElementException, \
    NoAlertPresentException
import os
import traceback
import time
import uuid


class basepage(object):
    server = u'http://127.0.0.1:5000'
    relative_url = u'/'
    params = u''
    url = urljoin(urljoin(server, relative_url), params)
    logpath = u'.'
    timeout = 60

    def __init__(self, context):
        self.driver = context.driver
        self.url = \
            urljoin(
                urljoin(
                    self.server
                    if context.server is None else context.server,
                    self.relative_url
                    if context.relative_url is None else context.relative_url
                ),
                self.params
                if context.params is None else context.params
            )
        self.timeout = context.timeout
        self.logpath = u'log' if context.logpath is None else context.logpath
        os.makedirs(context.logpath, exist_ok=True)

    def visit(self):
        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()
        except (TimeoutException, NoAlertPresentException):
            print(u"No alert")
        if self.driver.current_url is not None and \
                self.driver.current_url != self.url:
            self.driver.get(self.url)
        print(u'navigating:', self.url)

    def find_element(self, *loc):
        elems = self.driver.find_elements(*loc)
        if len(elems) < 1:
            raise AttributeError(str(loc), u': element not found!')
        return elems[0] if len(elems) == 1 else elems

    def hover(self, element):
        ActionChains(self.driver).move_to_element(element).perform()
        time.sleep(5)

    def __getattr__(self, elem):
        try:
            if elem in self.locator_dictionary.keys():
                try:
                    element = \
                        WebDriverWait(self.driver, self.timeout).until(
                            EC.presence_of_element_located(
                                self.locator_dictionary[elem])
                        )
                except(TimeoutException,
                       StaleElementReferenceException,
                       NoSuchElementException):
                    traceback.print_exc()
                return self.find_element(*self.locator_dictionary[elem])
        except AttributeError:
            super(basepage, self).__getattribute__(u'method_missing')(elem)

    def method_missing(self, elem):
        print(elem, u'Not found in ', self.url)

    def fill_field(self, fieldname, fieldtext, cleartext=True, multi_select=False):
        fieldname.location_once_scrolled_into_view
        if fieldname.tag_name == u'select':
            selected = False
            for option in fieldname.find_elements_by_tag_name(u'option'):
                if option.text.strip() == fieldtext.strip():
                    if multi_select:
                        if not option.is_selected():
                            ActionChains(self.driver).key_down(Keys.CONTROL).click(option).key_up(Keys.CONTROL).perform()
                    else:
                        option.click()
                    selected = True
                    break
            if not selected:
                try:
                    fieldname.find_element_by_xpath(
                        u'option[contains(text(),"{}")]'.format(fieldtext)).click()
                except AttributeError:
                    raise Exception(u'selection not found: ', fieldtext)
        elif fieldname.tag_name == u'input' or \
            fieldname.tag_name == u'textarea':
            if fieldname.get_attribute(u'type') == u'checkbox':
                if fieldname.is_selected() != eval(fieldtext):
                    fieldname.click()
            elif fieldname.get_attribute(u'type') == u'date':
                if self.driver.capabilities[u'browserName'] == u'chrome':
                    fieldtext = datetime.strptime(
                        fieldtext, u"%Y-%m-%d").strftime(u"%m/%d/%Y")
                fieldname.clear()
                fieldname.send_keys(fieldtext)
            else:
                if cleartext:
                    fieldname.clear()
                fieldname.send_keys(fieldtext)
