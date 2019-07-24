from selenium.webdriver.common.by import By
from .basepage import basepage


class newdatasetpage(basepage):

    def __init__(self, context):
        context.relative_url = u'dataset/new'
        super().__init__(context)

    locator_dictionary = {
        u'titleField': (By.ID, u'field-title'),
        u'editButton': (By.XPATH, u'//button[contains(text(), "Edit")]'),
        u'urlnameField': (By.ID, u'field-name'),
        u'descrptionField': (By.ID, u'field-notes'),
        u'tagsField': (By.ID, u's2id_field-tags'),
        u'orgField': (By.ID, u'select2-drop-mask'),
        u'visibilityField': (By.ID, u'field-private'),
        u'authorField': (By.ID, u'field-author'),
        u'emailField': (By.ID, u'field-author-email'),
        u'maintainerField': (By.ID, u'field-maintainer'),
        u'maintaineremailField': (By.ID, u'field-maintainer-email'),
        u'customFieldkey1': (By.ID, u'field-extras-0-key'),
        u'customFieldkey2': (By.ID, u'field-extras-1-key'),
        u'customFieldkey3': (By.ID, u'field-extras-2-key'),
        u'customFieldvalue1': (By.ID, u'field-extras-0-value'),
        u'customFieldvalue2': (By.ID, u'field-extras-1-value'),
        u'customFieldvalue3': (By.ID, u'field-extras-2-value'),
        u'addDataButton':
            (By.XPATH, u'//button[contains(text(), "Next: Add Data")]')
    }

    def fill_custom(self, fielddictionary):
        i = 1
        if len(fielddictionary) > 3:
            raise Exception(u'only 3 custom fields allow!')
        for fieldkey in fielddictionary.keys():
            keyname = u'customFieldkey' + str(i)
            valuename = u'customFieldvalue' + str(i)
            getattr(self, keyname).send_keys(fieldkey)
            getattr(self, valuename).send_keys(fielddictionary[fieldkey])
            i += 1

    def fill_required(self, fieldname, fieldtext):
        required_fields = {u'Title': self.titleField,
                           u'Description': self.descrptionField,
                           u'Visibility': self.visibilityField
                           }

        if fieldname in required_fields.keys():
            if required_fields[fieldname].tag_name == u'select':
                selected = False
                for option in \
                        required_fields[fieldname].\
                        find_elements_by_tag_name(u'option'):
                    if option.text == fieldtext:
                        option.click()
                        selected = True
                        break
                if not selected:
                    raise Exception(u'selection not found: ', fieldtext)
            elif required_fields[fieldname].tag_name == u'input' or \
                    required_fields[fieldname].tag_name == u'textarea':
                required_fields[fieldname].send_keys(fieldtext)
        else:
            raise Exception(u'filed not in the required list:', fieldname)
