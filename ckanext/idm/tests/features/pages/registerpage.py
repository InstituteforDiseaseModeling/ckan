from selenium.webdriver.common.by import By
from .basepage import basepage


class registerpage(basepage):

    def __init__(self, context):
        context.relative_url = u'/user/register'
        super().__init__(context)

    locator_dictionary = {
        u'usernameField': (By.ID, u'field-username'),
        u'fullnameField': (By.ID, u'field-fullname'),
        u'emailField': (By.ID, u'field-email'),
        u'passwordField': (By.ID, u'field-password'),
        u'passwordconfirmField': (By.ID, u'field-confirm-password'),
        u'createButton':
            (By.XPATH, u'//button[contains(text(),"Create Account")]')
    }

    def register(self, username, password, fullname, email):
        self.usernameField.send_keys(username)
        self.fullnameField.send_keys(fullname)
        self.emailField.send_keys(email)
        self.passwordField.send_keys(password)
        self.passwordconfirmField.send_keys(password)
        # need to by pass Captcha
        self.create.click()
