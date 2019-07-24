from selenium.webdriver.common.by import By
from .basepage import basepage
from.homepage import homePage


class loginpage(basepage):

    def __init__(self, context):
        context.relative_url = "/user/login"
        super().__init__(context)

    locator_dictionary = {
        "usernameField": (By.ID, 'field-login'),
        "passwordField": (By.ID, 'field-password'),
        "remembermeCheckbox": (By.ID, 'field-remember'),
        "loginButton": (By.XPATH, '//button[contains(text(), "Login")]'),
        "loggedinText": (By.XPATH, '//*[contains(text(),"already logged in")]')
    }

    def login(self, username, password):
        loggedin = None
        try:
            loggedin = self.loggedinText
        except:
            self.usernameField.clear()
            self.usernameField.send_keys(username)
            self.passwordField.clear()
            self.passwordField.send_keys(password)
            if self.remembermeCheckbox.get_attribute('checked'):
                self.remembermeCheckbox.click()
            self.loginButton.click()
