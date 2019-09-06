@demo
@UI
Feature: Add datasets for editors
  # Refer to https://wiki.idmod.org/display/SP/Phase+1%3A+Data+Catalog+Prototype
  Background:
    Given I am registered
    When I am logged in
    And I am added to the research group as editor
      | Research Group  |
      | Test Automation |
    And a list of pre-defined "Tags" has been loaded in the system
      | Tags      |
      | Population|
      | Measles   |
      | Raw       |
      | Pakistan  |
    And a list of pre-defined "Topics" has been loaded in the system
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


  @addDataset
  Scenario:Create Dataset
    Given I have the file
    Given I have dataset info
    When I click "Add Dataset"
    Then I am redirected to the Create Dataset page


  @allRequiredFields
  Scenario: Required Field
    #all required fields as shown in the table
    Given I am ready to create dataset (tag:addDataset)
    Then I must set all required dataset fields
      | fields            | values                          |
      | Title             | ERA5 daily files                |
      | Description       | Daily files from ERA5 hourly.   |
      | Maintainer email  | dlukacevic@idmond.org           |
      | Purpose           | Raw Data                        |
      | Research Group    | Test Automation                 |
      | Disease           | Any                             |
      | Start Date        | 1979-01-01                      |
      | End Date          | 2018-12-31                      |
      | Location          | World                           |
      | Publisher         | IDM                             |
      | Acquisition Date  | 2019-03-01                      |
      | Version           | 1.0                             |
      | Visibility        | Public                          |
      | Restricted        | False                           |
      | License           | Creative Commons Attribution    |


  Scenario Outline: Required Field in depth
    #some required fields must have preset values
    Given I am ready to create dataset (tag:addDataset)
    Then I must set required dataset fields
      | fields            | values                          |
      | Title             | ERA5 daily files.               |
      | Description       | Daily files from ERA5 hourly.   |
      | Maintainer email  | dlukacevic@idmond.org           |
      | Research Group    | Data Services                   |
      | Start Date        | 1979-01-01                      |
      | End Date          | 2018-01-01                      |
      | Acquisition Date  | 2019-03-01                      |
      | Version           | 1.0                             |
      | License           | Creative Commons Attribution    |


    And I must set required Purpose to <purpose>
    Examples:
      | purpose         |
      | Raw Data        |
      | Project Files   |
      | Published Paper |

    And I must set required Disease to <disease>
    Examples:
      | disease   |
      | Any       |
      | Cholera   |
      | Ebola     |
      | HAT       |
      | HIV       |
      | Malaria   |
      | Measles   |
      | Pneumonia |
      | Polio     |
      | TB        |
      | Typhoid   |

    And I must set required Location to <location>
    Examples:
      | location                                |
      | Pakistan                                |
      | Pakistan, Nigeria, Indonesia, Ethiopia  |
      | World                                   |

    And I must set required Visibility to <visibility>
    Examples:
      |visibility  |
      |Private     |
      |Public      |

    And I must set required Restricted to <restricted>
    Examples:
      | restricted |
      | True       |
      | False      |

    And I must set required Publisher to <publisher>
    Examples:
      | publisher |
      | IDM       |
      | WHO       |


  Scenario: Optional Field
    Given I have filled in all required fields(tag:allRequiredFields)
    When I set all optional dataset fields
      | fields            | values                          |
      | Tags              | temperature rainfall humidity   |
      | Quality Issues    | Quality: 1979-01-01 is bad      |
      | Origin URL        | https://wiki.idmod.org/display/SP/ERA5+Data+Sets  |

    Then I can click "Add Data"


  Scenario Outline: Tag
    #Tag must have preset values
    Given I have filled in all required fields(tag:allRequiredFields)
    When I start to type a tag that is a pre-defined <tags>
    Then The system suggests the existing tag:<tags>
    And I can select the pre-existing <tags> to auto-complete the tag

    Examples:
      | tags        |
      | Population  |
      | Measles     |
      | Raw         |
      | Pakistan    |


   Scenario Outline: Spatial coverage for location
    Given I have filled in all required fields(tag:allRequiredFields)
	  When I fill out the Spatial section for <location>
	  Then I will see an optional field <location_dot_name> to enter text

    Examples:
      | location    | location_dot_name   |
      | Burkina     | Africa:Burkina Faso |


  @addDataRequiredFields
  Scenario: Create Data dataset with link
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
    And I can click "Finish"


  Scenario: Create Data dataset with Upload
    Given I have filled in all required fields(tag:allRequiredFields)
    When I can click "Add Data"
    Then I can click "Upload" and select a local file
    And I must set required resource fields
      | fields            | values            |
      | Type              | Code              |
      | Name              | Acquisition email |

    And I can set optional resource fields
      | fields            | values                          |
      | Description       | When they told us about ERA5    |
      | Format            | email                           |

    And I can click "Finish"


  Scenario Outline: Resource fields in-depth
     Given I have filled in all required fields(tag:allRequiredFields)
     When I can click "Add Data"
     Then I can set required "Type" <type>
     Examples:
      | type  |
      | Data  |
      | Code  |
      | Doc   |
      | Paper |
      | Origin|
      | Other |

  Scenario Outline: Topic
    #Topic must have preset values
    #Topic is associated after dataset is created
    Given I have created a dataset with resource (tag:addDataRequiredFields)
    When I click on the Topic tab on dataset page
    Then A drop-down of available <topic> are listed
    And I can select the pre-existing <topic> to auto-complete their topic field
    Examples:
      | topic                                                     |
      | Incidence Data                                            |
      | Mortality                                                 |
      | Population                                                |
      | Shapefiles                                                |
      | Births                                                    |
      | Climate                                                   |
      | MICS - Multiple Indicator Cluster Surveys                 |
      | VTS - Vertical Transmission cohort Study                  |
      | SIAs - Supplemental immunisation activity campaigns       |
      | PCCS - Post Campaign Coverage Surveys                     |
