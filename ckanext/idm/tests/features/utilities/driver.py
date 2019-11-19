# encoding: utf-8

import os
import uuid
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


chorme_driver_root = os.path.join(os.path.dirname(__file__),
                                  u'../drivers/chrome')
firefox_driver_root = os.path.join(os.path.dirname(__file__),
                                   u'../drivers/firefox')


def firefox_driver(context):
    firefox_driver_path = \
        os.path.join(firefox_driver_root,
                     context.driver_version + u'/geckodriver.exe')
    driver = webdriver.Firefox(
        executable_path=firefox_driver_path
        if context.driverpath is None else context.driverpath)
    driver.maximize_window()
    print(u'driver:', driver.name)
    context.driver = driver
    yield context.driver
    driver.quit()


def chrome_driver(context):
    chorme_driver_path = \
        os.path.join(chorme_driver_root,
                     context.driver_version + u'/chromedriver.exe')
    chrome_options = Options()
    chrome_options.add_argument(u"--start-maximized")
    chrome_options.add_argument(u"--disable-gpu")
    chrome_options.add_argument(u"--disable-extensions")
    chrome_options.add_argument(u'--disable-useAutomationExtension')

    driver = webdriver.Chrome(
        executable_path=chorme_driver_path
        if context.driverpath is None else context.driverpath, chrome_options=chrome_options)


    print(u'driver:', driver.name)
    context.driver = driver
    yield context.driver
    driver.quit()


def screenshot(context):
    filepath = os.path.join(context.logpath, str(uuid.uuid4()) + u'.png')
    context.driver.save_screenshot(filepath)
    print(u'saving screenshot to: ', filepath)
