from selenium.webdriver.common.by import By
from .basepage import basepage

class newdatasetpage(basepage):

    def __init__(self, context):
        context.relative_url="dataset/new"
        super().__init__(context)

    locator_dictionary = {
        "titleField" : (By.ID, 'field-title'),
        "editButton" : (By.XPATH, '//button[contains(text(), "Edit")]'),
        "urlnameField" : (By.ID, 'field-name'),
        "descrptionField" : (By.ID, 'field-notes'),
        "tagsField" : (By.ID, 's2id_field-tags'),
        "orgField" :(By.ID, 'select2-drop-mask'),
        "visibilityField" : (By.ID, 'field-private'),
        "authorField" : (By.ID, 'field-author'),
        "emailField" : (By.ID, 'field-author-email'),
        "maintainerField" : (By.ID, 'field-maintainer'),
        "maintaineremailField" : (By.ID, 'field-maintainer-email'),
        "customFieldkey1" : (By.ID, 'field-extras-0-key'),
        "customFieldkey2": (By.ID, 'field-extras-1-key'),
        "customFieldkey3": (By.ID, 'field-extras-2-key'),
        "customFieldvalue1": (By.ID, 'field-extras-0-value'),
        "customFieldvalue2": (By.ID, 'field-extras-1-value'),
        "customFieldvalue3": (By.ID, 'field-extras-2-value'),
        "addDataButton" : (By.XPATH, '//button[contains(text(), "Next: Add Data")]')
    }

    def fillCustom(self, fielddictionary):
        i = 1
        if len(fielddictionary) > 3:
            raise Exception("only 3 custom fields allow!")
        for fieldkey in fielddictionary.keys():
            keyname = "customFieldkey" + str(i)
            valuename= "customFieldvalue" + str(i)
            getattr(self, keyname).send_keys(fieldkey)
            getattr(self, valuename).send_keys(fielddictionary[fieldkey])
            i+=1

    def fillRequired(self, fieldname, fieldtext):
        required_fields = {"Title" : self.titleField,
                           "Description": self.descrptionField,
                           "Visibility" : self.visibilityField
                           }

        if fieldname in required_fields.keys():
            if required_fields[fieldname].tag_name == "select":
                selected = False
                for option in required_fields[fieldname].find_elements_by_tag_name('option'):
                    if option.text == fieldtext:
                        option.click()
                        selected = True
                        break
                if not selected:
                    raise Exception("selection not found: ", fieldtext)
            elif required_fields[fieldname].tag_name == "input" or required_fields[fieldname].tag_name == "textarea" :
                required_fields[fieldname].send_keys(fieldtext)
        else:
            raise Exception("filed not in the required list:", fieldname)
