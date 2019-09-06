from selenium.webdriver.common.by import By
from .basepage import basepage
from.homepage import homepage


class loginpage(basepage):

    def __init__(self, context):
        context.relative_url = u'/user/login'
        super(loginpage, self).__init__(context)

    locator_dictionary = {
        u'usernameField': (By.ID, u'field-login'),
        u'passwordField': (By.ID, u'field-password'),
        u'remembermeCheckbox': (By.ID, u'field-remember'),
        u'loginButton': (By.XPATH, u'//button[contains(text(), "Login")]'),
        u'loggedinText':
            (By.XPATH, u'//*[contains(text(),"already logged in")]')
    }

    def login(self, username, password):
        loggedin = None
        try:
            loggedin = self.loggedinText
            if loggedin is None:
                raise AttributeError(u"not yet login")
        except AttributeError:
            self.usernameField.clear()
            self.usernameField.send_keys(username)
            self.passwordField.clear()
            self.passwordField.send_keys(password)
            if self.remembermeCheckbox.get_attribute(u'checked'):
                self.remembermeCheckbox.click()
            self.loginButton.click()
