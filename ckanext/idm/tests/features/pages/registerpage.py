from selenium.webdriver.common.by import By
from .basepage import basepage


class registerpage(basepage):

    def __init__(self, context):
        context.relative_url = "/user/register"
        super().__init__(context)

    locator_dictionary = {
        "usernameField": (By.ID, 'field-username'),
        "fullnameField": (By.ID, 'field-fullname'),
        "emailField": (By.ID, 'field-email'),
        "passwordField": (By.ID, 'field-password'),
        "passwordconfirmField": (By.ID, 'field-confirm-password'),
        "createButton":
            (By.XPATH, '//button[contains(text(),"Create Account")]')
    }

    def register(self, username, password, fullname, email):
        self.usernameField.send_keys(username)
        self.fullnameField.send_keys(fullname)
        self.emailField.send_keys(email)
        self.passwordField.send_keys(password)
        self.passwordconfirmField.send_keys(password)
        # need to by pass Captcha
        self.create.click()
