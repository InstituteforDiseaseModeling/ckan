@demo
@UI
Feature: Create a new dataset
  As a researcher,
  I want to save and tag my dataset for projects

  Background:
    Given The use has registered
    Given The user is logged in
    Given The user is added to the organization
    Given I have a link for a dataset
     | name  | description | url |
     | ERA5  | weather data| https://www.ecmwf.int/en/forecasts/datasets/reanalysis-datasets/era5|


  Scenario: Add a dataset from third party source
    When I click "new dataset"
    Then I am required to fill values in these fields
      | fields      | values                |
      | Description | This is a useful doc  |
      | Title       | Weather Files         |
      | Visibility  | Public                |

    And I can optionally add up to 3 fields with values
      | fields        | values                |
      | collaborator  | Mr.Gates              |
      | association   | BGMF                  |
      | ISO number    | 12345                 |

    And I can click add data and enter name, description  and url of the third party source

  Scenario: Add a dataset by upload
    When I click "new dataset"
    Then I am required to fill values in these fields
      | fields      | values                |
      | Description | This is a useful doc  |
      | Title       | Weather Files         |
      | Visibility  | Public                |
    And I can click add data upload myfile

  Scenario Outline: Update dataset
    Given I know my dataset url
    When I Click manage
    And I update these <field>
    Then I can update dataset

    Examples:
      | field       |
      | Description |
      | Title       |
      | Visibility  |


  Scenario: Delete dataset
    Given I know my dataset url
    When I Click manage
    And I click delete
    Then the dataset url should now be invalid
	
  Scenario: Set required field "Title"
    Given There is a data set "Title" field
    When I create a new dataset
    Then I am required to fill in the "Title" field
	
  Scenario: Set required field "Description"
  Given There is a data set "Description" field
  When I create a new dataset
  Then I am required to fill in the "Description" field
  
  Scenario: Set optional field "Notes"
  Given There is a data set "Notes" field
  When I create a new dataset
  Then I can optionally fill in the "Notes" field
  
  Scenario: Set required field "Maintainer email"
  Given There is a data set "Maintainer email" field
  When I create a new dataset
  Then I am required to fill in the "Maintainer email" field
  
  Scenario: Set required field "Type"
  Given There is a data set "Categorization Type" field
  When I create a new dataset
  Then I am required to select the options in the drop down for the <Type> field
	
  Scenario Outline: Set required field "Research Group"
    Given There is a list of Research Groups to pick from
    When User selects a <Research Group>
    Then User is required to fill in the <Research Group> field

  Examples: 
      |Research Group                | 
      |Applied Math                  |
      |Data Dynamics and Analytics   |
      |Health Econ                   |
      |HIV/TB                        |
      |Malaria                       |
      |Measles                       |
      |MNCH                          |
      |SMUG (Polio, Vaccine Delivery)|
      |Malaria                       |
	  
  Scenario Outline: Set required field "Disease"
  Given There is a list of Diseases to pick from
  When User selects a <Disease>
  Then User is required to fill in the <Disease> field

  Examples: 
      |Disease                       | 
	  |Dengue                        |
	  |Ebola                         |
	  |Enteric                       |
      |HIV                           |
	  |Flu                           |
      |Malaria                       |
      |Measles                       |
      |Polio                         |
      |TB                            |

  Background:
  	Given a list of pre-defined "Tags" has been loaded in the system
    
  Scenario Outline: Set "Tags" for a data set
    Given There is a Tags field
    When User starts to type a tag that is a pre-defined <tags>
    Then The system suggests the existing <tags>
    Then User can select the pre-existing <tags> to auto-complete their tag

  Examples: 
     | Tags           | Values      |
     | Category         | Population  |  
     | Disease          | Measles     |  
     | Stage            | Raw         |  
     | Spatial coverage | Pakistan    | 
	 
  Background:
  	Given a list of pre-defined "Topics" has been loaded in the system
    
  Scenario Outline: Set a "Topic" for a data set
    Given There is a Topic field
    When User clicks on the Topic field
    Then The a drop-down of available <topic> are listed
    Then User can select the pre-existing <topic> to auto-complete their topic field

  Examples: 
     | Topic           |
     | Incidence Data  |  
     | Mortality       | 
     | Population      |  
     | Serosurvey      |
	 | Shapefiles	   |
	 | Births          |
	 | Climate         |

  Scenario: User enters a data set with temporal coverage
    Given I enter a data set with temporal coverage
    When I fill out the <Temporal> coverage field
    Then I should have the option to provide a <Start Date> and <End Date> the data is for
	
  Scenario Outline: User enters data set with spatial coverage
    Given I enter a data set for a specific country or covers a set of countries
	When I fill out the Spatial section
	Then I will be required to select a <Country>, Countries, or World to indicate a world-wide dataset
	
  Examples:
  | Country                                 |
  | Pakistan                                |
  | Pakistan, Nigeria, Indonesia, Ethiopia  |
  | World                                   |
  
  Scenario Outline: User enters data set with spatial coverage
    Given I enter a data set for a specific LGA or a set of LGAs
	When I fill out the Spatial section
	Then I will be an optional field <LGA> to select <LGA>
	
  Examples:
  | LGA                                                                                                       |
  | Asia:PAKISTAN:GILGIT BALTISTAN:GHANCHE                                                                    |
  | Asia:PAKISTAN:GILGIT BALTISTAN:GHANCHE, Asia:PAKISTAN:GILGIT BALTISTAN:GHIZER, Asia:PAKISTAN:SINDH:GHOTKI |
  
  Scenario Outline: User enters data set with spatial coverage
    Given I enter a data set for a specific place
	When I fill out the Spatial section
	Then I will be an optional field <place> to enter text
	
  Examples:
  | Place                                 |
  | Lake Kariba                           |

  Scenario Outline: Set required field "Publisher" for the data
    Given User enters a new data
    When The user enters the <Publisher> for the data
    Then They can select a <Publisher> that has been pre-defined in the system

  Examples: 
      |Publisher   |
      |IDM         |
      |WHO         |
	  
  Scenario: Set required field "Point of Contact"
    Given User enters new data
    When The user enters the "Point of Contact" for the data
    Then This field is required
    Then The user can pick from IDM users set in the system
	
  Scenario Outline: Set required field "Terms of Use"
    Given User enters new data
     When The user selects the "Terms of Use" field
     Then They are required to select the options in this drop down
     Then They have an option to fill in a free-form text box or
     Then They have the option to link evidence we have rights to the file (e.g. email from the source)

  Example: 
      |options      |
      |Unrestricted |
      |Restricted   |
	  
  Scenario: Manage Research Group
  Given User needs to create a new Research Group
  When The user selects "Add Group"
  Then The user will be required to fill in a <Name>, <URL>
  Then The user can optionally fill in a <Description>
  Then The user can optionally upload an image and set a link
  Then The user must select the button "Create Group" to save the new Research Group
  
  Scenario: Manage Topics
  Given User needs to create a new Topic
  When The user selects "Add Topic"
  Then The user will be required to fill in a <Name>, <URL>
  Then The user can optionally fill in a <Description>
  Then The user can optionally upload an image and set a link
  Then The user must select the button "Create Topic" to save the new Topic
 
