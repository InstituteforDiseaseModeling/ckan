from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .newdatasetpage import newdatasetpage


class editdatasetpage(newdatasetpage):
    def __init__(self, context):
        datasetname = context.datasetname
        context.relative_url = u'/dataset/edit/' + u'/{}'.format(datasetname)
        super(editdatasetpage, self).__init__(context)

    locator_dictionary = {
        u'editMetadataLink': (By.PARTIAL_LINK_TEXT, u'Edit metadata'),
        u'editResourceLink': (By.PARTIAL_LINK_TEXT, u'Resources'),
        u'addResourceLink': (By.PARTIAL_LINK_TEXT, u'Add new resource'),
        u'updateDatasetButton': (By.XPATH, u'//button[contains(text(),"Update Dataset")]'),
        u'deleteLink': (By.PARTIAL_LINK_TEXT, u'Delete'),
        u'deleteConfirmButton': (By.XPATH, u'//button[contains(text(),"Confirm")]'),
        u'deleteCancelButton': (By.XPATH, u'//button[contains(text(),"Cancel)]'),
        u'resourceElems': (By.CSS_SELECTOR, u'li.resource-item a.heading'),
        # metadata fields
        u'titleField': (By.ID, u'field-title'),
        u'editButton': (By.XPATH, u'//div[@class="slug-preview"]//button[contains(text(), "Edit")]'),
        u'urlnameField': (By.ID, u'field-name'),
        u'descrptionField': (By.ID, u'field-notes'),
        u'maintaineremailField': (By.ID, u'field-maintainer_email'),
        u'purposeField': (By.ID, u'field-purpose'),
        u'researchField': (By.ID, u'field-organizations'),
        u'visibilityField': (By.ID, u'field-private'),
        u'diseaseField': (By.ID, u'field-disease'),
        u'tagsField': (By.ID, u'field-tag_string'),
        u'qualityField': (By.ID, u'field-quality'),
        u'qualitynoteField': (By.ID, u'field-quality_notes'),
        u'startdateField': (By.ID, u'field-ext_startdate'),
        u'enddateField': (By.ID, u'field-ext_enddate'),
        u'temporalgapField': (By.ID, u'field-temporal_gaps'),
        u'locationField': (By.ID, u'field-location'),
        u'spatialgapField': (By.ID, u'field-spatial_gaps'),
        u'spatialField': (By.ID, u'field-spatial'),
        u'spatialResField': (By.ID, u'field-spatial_resolution'),
        u'spatialModeField': (By.ID, u'field-spatial_mode-manual'),
        u'publisherField': (By.ID, u'field-publisher'),
        u'urlField': (By.ID, u'field-url'),
        u'acquisitiondateField': (By.ID, u'field-acquisition_date'),
        u'versionField': (By.ID, u'field-version'),
        u'restrictedCheckbox': (By.ID, u'field-request_access-maintainer'),
        u'licenseField': (By.ID, u'field-license_id'),
        }

    def delete(self):
        self.deleteLink.click()
        wait = WebDriverWait(self.driver, 10)
        elem = wait.until(EC.element_to_be_clickable((By.XPATH, u'//button[contains(text(),"Confirm")]')))
        elem.click()

