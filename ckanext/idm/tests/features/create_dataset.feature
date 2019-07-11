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
	
  Scenario: Set required field "Name"
    Given There is a data set "Name" field
    When I create a new dataset
    Then I am required to fill in the "Name" field
	
  Scenario: Set required field "Research Team"
    Given There is a list of Research Teams to pick from
    When User selects a "Research Team"
    Then User is required to fill in the "Research Team" field

  Examples: 
      |Research Teams                | 
      |Applied Math                  |
      |Data Dynamics and Analytics   |
      |Health Econ                   |
      |HIV/TB                        |
      |Malaria                       |
      |Measles                       |
      |MNCH                          |
      |SMUG (Polio, Vaccine Delivery)|
      |Malaria                       |

  Background:
  	Given a list of pre-defined "Tags" has been loaded in the system
    
  Scenario Outline: Set "Tags" for a data set
    Given There is a Tags field
    When User starts to type a tag that is a pre-defined tag
    Then The system suggests the existing tag
    Then User can select the pre-existing tag to auto-complete their tag

  Examples: 
     | fields           | values      |
     | Category         | Population  |  
     | Disease          | Measles     |  
     | Stage            | Raw         |  
     | Spatial coverage | Pakistan    | 

  Scenario: User enters a data set with temporal coverage
    Given I enter a data set with temporal coverage
    When I fill out the Temporal coverage field
    Then I should have the option to provide a year or date range between years the data is for

  Scenario Outline: Set required field "Source" for the data
    Given User enters a new data
    When The user enters the Source for the data
    Then They can select an organization that has been pre-defined in the system

  Examples: 
      |options     |
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
