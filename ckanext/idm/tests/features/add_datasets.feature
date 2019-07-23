@demo
@UI
Feature: Add datasets for editors
  # Refer to https://wiki.idmod.org/display/SP/Phase+1%3A+Data+Catalog+Prototype
  Background:
    Given The use has registered
    Given The user is logged in
    Given The user is added to the research group as editor
      | Research Group    | Data Services |
    Given a list of pre-defined "Tags" has been loaded in the system
    Given a list of pre-defined "Topics" has been loaded in the system


  @addDataset
  Scenario:Create Dataset
    Given I have the file
    Given I have dataset info
       | name  | description | url                                                                  |
       | ERA5  | weather data| https://www.ecmwf.int/en/forecasts/datasets/reanalysis-datasets/era5 |

    When I click "Add Dataset"
    Then I am redirected to the Create Dataset page


  @allRequiredFields
  Scenario:Required Field
    #all required fields as shown in the table
    Given I am ready to create dataset (tag:addDataset)
    Then I must set all required dataset fields
      | fields            | values                          |
      | Title             | ERA5 daily files.               |
      | Description       | Daily files from ERA5 hourly.   |
      | Maintainer email  | dlukacevic@idmond.org           |
      | Type              | Data                            |
      | Research Group    | Data Services                   |
      | Disease           | Any                             |
      | Start Date        | 1979                            |
      | End Date          | 2018                            |
      | Country           | World                           |
      | Publisher         | IDM                             |
      | Acquisition Date  | 2019-03-01                      |
      | Version           | 1.0                             |
      | Visibility        | Public                          |
      | Restricted        | False                           |
      | License           | default                         |


  Scenario: Required Field in depth
    #some required fields must have preset values
    Given I am ready to create dataset (tag:addDataset)
    Then I must set required dataset fields
      | fields            | values                          |
      | Title             | ERA5 daily files.               |
      | Description       | Daily files from ERA5 hourly.   |
      | Maintainer email  | dlukacevic@idmond.org           |
      | Research Group    | Data Services                   |
      | Start Date        | 1979                            |
      | End Date          | 2018                            |
      | Acquisition Date  | 2019-03-01                      |
      | Version           | 1.0                             |
      | License           | default                         |


    And I must set required "Type"
      | values  |
      | Data    |
      | Project |
      | Paper   |

    And I must set required "Disease"
      | Disease                       |
      | Dengue                        |
      | Ebola                         |
      | Enteric                       |
      | HIV                           |
      | Flu                           |
      | Malaria                       |
      | Measles                       |
      | Polio                         |
      | TB                            |

    And I must set required "Country"
      | Country                                 |
      | Pakistan                                |
      | Pakistan, Nigeria, Indonesia, Ethiopia  |
      | World                                   |

    And I must set required "Visibility"
      |Visibility  |
      |Private     |
      |Public      |

    And I must set required "Restricted"
      | Restricted |
      | True       |
      | False      |

    And I must set required "Publisher"
      | IDM |
      | WHO |


  Scenario: Optional Field
    Given I have filled in all required fields(tag:allRequiredFields)
    When I set all optional dataset fields
      | fields            | values                          |
      | Tags              | temperature rainfall humidity   |
      | Notes             | Quality: 1979-01-01 is bad      |
      | Topic             | Climate                         |
      | Origin URL        | https://wiki.idmod.org/display/SP/ERA5+Data+Sets  |

    Then I can click "Add Data"


  Scenario Outline: Topic
    #Topic must have preset values
    Given I have filled in all required fields(tag:allRequiredFields)
    When I click on the <Topic> field
    Then A drop-down of available <Topic> are listed
    Then I can select the pre-existing <Topic> to auto-complete their topic field
    Examples:
      | Topic                                                     |
      | Incidence Data                                            |
      | Mortality                                                 |
      | Population                                                |
      | Shapefiles                                                |
      | Births                                                    |
      | Climate                                                   |
      | MICS - Multiple Indicator Cluster Surveys                 |
      | VTS - Vertical Transmission cohort Study                  |
      | SIAs -  Supplemental immunisation activity campaigns      |
      | PCCS - Post Campaign Coverage Surveys                     |


  Scenario Outline: Tag
    #Tag must have preset values
    Given I have filled in all required fields(tag:allRequiredFields)
    When I start to type a tag that is a pre-defined <Tags>
    Then The system suggests the existing <Tags>
    And I can select the pre-existing <Tags> to auto-complete the tag

    Examples:
      | Tags             | Values      |
      | Category         | Population  |
      | Disease          | Measles     |
      | Stage            | Raw         |
      | Spatial coverage | Pakistan    |


  Scenario Outline: spatial coverage
    Given
    And I have selected one or more <Country>
    When I fill out the Spatial section for LGA
	  Then I will see an optional field <LGA> to select <LGA>
    Then I should not see the <ExcludedLGA> because <Country> does not contain <ExcludedLGA>
    Examples:
      | Country            | LGA                                                                                                       | ExcludedLGA                          |
      | Pakistan           | Asia:PAKISTAN:GILGIT BALTISTAN:GHANCHE                                                                    | asia:indonesia:yogyakarta:yogyakarta |
      | Pakistan           | Asia:PAKISTAN:GILGIT BALTISTAN:GHANCHE, Asia:PAKISTAN:GILGIT BALTISTAN:GHIZER, Asia:PAKISTAN:SINDH:GHOTKI | asia:indonesia:yogyakarta:yogyakarta |
      | Pakistan, Indonesia| Asia:PAKISTAN:GILGIT BALTISTAN:GHANCHE, asia:indonesia:kalimantan timur:tarakan                           | Africa:Burkina Faso:Banwa:Kouka      |
      | World              | asia:indonesia:yogyakarta:yogyakarta                                                                      | None                                 |

   Scenario Outline: spatial coverage for place
    Given I have filled in all required fields(tag:allRequiredFields)
	  When I fill out the Spatial section for Place
	  Then I will see an optional field <Place> to enter text

    Examples:
      | Place                                 |
      | Lake Kariba                           |


  Scenario: Custom Field
    Given I have filled in all required fields(tag:allRequiredFields)
    When I optionally add up to 3 fields with values
      | fields            | values                          |
      | Collaborator      | Mr.Smith                        |
      | Association       | UW                              |
      | ISO number        | 12345                           |
     Then I can click "Add Data"


  @addDataRequiredFields
  Scenario: Create Data dataset with link.
    Given I have filled in all required fields(tag:allRequiredFields)
    When I can click "Add Data"
    And I can click "Link"
    And I must set required resource fields
      | fields            | values                                            |
      | URL               | https://climate.copernicus.eu/climate-reanalysis  |
      | Type              | Data                                              |
      | Name              | ERA5 hourly                                       |
    And I can set optional resource fields
      | fields            | values                          |
      | Description       | ERA5 hourly data for 1979-2018  |
      | Format            | netCDF                          |
    Then I can click "Save & add another"


  Scenario: Create Data dataset with Upload
    Given I am ready to upload data (tag:addDataRequiredFields)
    Then I can click "Upload" and select a local file
    And I must set required resource fields
      | fields            | values                          |
      | Type              | Origin                          |
      | Name              | Acquisition email               |

    And I can set optional resource fields
      | fields            | values                          |
      | Description       | When they told us about ERA5    |
      | Format            | email                           |

    And I can click "Finish"
