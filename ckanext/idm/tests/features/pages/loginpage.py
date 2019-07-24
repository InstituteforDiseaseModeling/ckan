from selenium.webdriver.common.by import By
from .basepage import basepage
from.homepage import homePage


class loginpage(basepage):

    def __init__(self, context):
        context.relative_url = u'/user/login'
        super().__init__(context)

    locator_dictionary = {
        u'usernameField': (By.ID, u'field-login'),
        u'passwordField': (By.ID, u'field-password'),
        u'remembermeCheckbox': (By.ID, u'field-remember'),
        u'loginButton': (By.XPATH, u'//button[contains(text(), "Login")]'),
        u'loggedinText': (By.XPATH, u'//*[contains(text(),"already logged in")]')
    }

    def login(self, username, password):
        loggedin = None
        try:
            loggedin = self.loggedinText
        except AttributeError:
            self.usernameField.clear()
            self.usernameField.send_keys(username)
            self.passwordField.clear()
            self.passwordField.send_keys(password)
            if self.remembermeCheckbox.get_attribute('checked'):
                self.remembermeCheckbox.click()
            self.loginButton.click()
