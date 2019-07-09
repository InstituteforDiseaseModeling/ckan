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





