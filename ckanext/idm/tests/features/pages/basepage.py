import os
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import traceback
import time
import uuid


class basepage(object):
    server = "http://127.0.0.1:5000"
    relative_url = "/"
    params = ""
    url = urljoin(urljoin(server, relative_url), params)
    logpath = "."
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
        self.logpath = 'log' if context.logpath is None else context.logpath
        os.makedirs(context.logpath, exist_ok=True)

    def visit(self):
        if self.driver.current_url is not None and \
                self.driver.current_url != self.url:
            self.driver.get(self.url)
        print("navigating:", self.url)

    def find_element(self, *loc):
        elems = self.driver.find_elements(*loc)
        if len(elems) < 1:
            raise AttributeError(str(*loc), ": element not found!")
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
                                self.locator_dictionary[elem]) and
                            EC.visibility_of_element_located(
                                self.locator_dictionary[elem])
                        )
                except(TimeoutException,
                       StaleElementReferenceException,
                       NoSuchElementException):
                    traceback.print_exc()
                return self.find_element(*self.locator_dictionary[elem])
        except AttributeError:
            super(basepage, self).__getattribute__("method_missing")(elem)

    def method_missing(self, elem):
        print(elem, "Not found in ", self.url)
