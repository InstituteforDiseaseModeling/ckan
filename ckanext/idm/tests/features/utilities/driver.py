import os
import uuid
from selenium import webdriver

chorme_driver_root = os.path.join(os.path.dirname(__file__),
                                  "../drivers/chrome")
firefox_driver_root = os.path.join(os.path.dirname(__file__),
                                   "../drivers/firefox")


def firefox_driver(context):
    firefox_driver_path = \
        os.path.join(firefox_driver_root,
                     context.driver_version + "/geckodriver.exe")
    driver = webdriver.Firefox(
        executable_path=firefox_driver_path
        if context.driverpath is None else context.driverpath)
    print("driver:", driver.name)
    context.driver = driver
    yield context.driver
    driver.quit()


def chrome_driver(context):
    chorme_driver_path = \
        os.path.join(chorme_driver_root,
                     context.driver_version + "/chromedriver.exe")
    driver = webdriver.Chrome(
        executable_path=chorme_driver_path
        if context.driverpath is None else context.driverpath)
    print("driver:", driver.name)
    context.driver = driver
    yield context.driver
    driver.quit()


def screenshot(context):
    filepath = os.path.join(context.logpath, str(uuid.uuid4()) + ".png")
    context.driver.save_screenshot(filepath)
    print("saving screenshot to: ", filepath)
