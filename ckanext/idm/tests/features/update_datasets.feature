@demo
@UI
Feature: Update dataset
  As a researcher,
  I want to be able to update the dataset that was created previously
  This includes metadata and resources

 Background:
    Given I am logged in

 Scenario: Change Topic Association
   Given the dataset is created and associated with a topic
   When I am on dataset page
   And I can change the topic association from the topic tab

 @pri1
 Scenario Outline: Update dataset metadata
   Given I have a dataset created with <data_values> for <data_fields>
   When I am on dataset page
   And I click Manage
   Then I enter <new_values> in <data_fields> to update dataset and expect changes to be there
   Examples:
     | data_fields       | data_values                            | new_values      |
     | Title             | ERA5 daily files.                      | ERA5            |
     | Description       | Daily files from ERA5 hourly.          | changed         |
     | Maintainer email  | dlukacevic@idmond.org                  | xyz@abc.com     |
     | Purpose           | Raw Data                               | Published Paper |
     | Quality Rating    | Good                                   | Great           |
     | Quality Issues    | Unknown                                | Passed          |
     | Disease           | Any                                    | Malaria         |
     | Start Date        | 1979-01-01                             | 1980-01-01      |
     | End Date          | 2018-12-31                             | 1980-01-02      |
     | Location          | World                                  | USA             |
     | Publisher         | IDM                                    | Unknown         |
     | Acquisition Date  | 2019-03-01                             | 2019-01-01      |
     | Version           | 1.0                                    | 2.0             |
     | Visibility        | Public                                 | Private         |
     | Restricted        | False                                  | True            |
     | License           | reative Commons CCZero                 | Creative Commons Attribution  |
     | Temporal Gaps     | None                                   | Missing Jan     |
     | Spatial Gaps      | None                                   | TBD             |
     | Spatial Extent    | {"type":"Point","coordinates":[1, 30]} | {"type":"Point","coordinates":[2, 29]}  |


   @pri1
    Scenario: Delete dataset
     Given I have created a dataset with resource (tag:addDataRequiredFields)
     When I am on dataset page
     And I click Manage
     Then I can delete the dataset

   @pri1
   Scenario: Delete resource
     Given I have created a dataset with resource (tag:addDataRequiredFields)
     When I am on dataset page
     And I click Manage
     And I go the Edit Resource tab
     Then I can delete the resource

   @pri1
   Scenario:  Add resource
     Given I have created a dataset with resource (tag:addDataRequiredFields)
     When I am on dataset page
     And I click Manage
     And I go the Add Resource tab
     And I add a new resource
     Then I should see both old and new resources

   @pri1
   Scenario Outline: Edit resource metadata
     Given I have created a dataset with resource (tag:addDataRequiredFields)
     When I am on dataset page
     And I click Manage
     And I go the Edit Resource tab
     And I change <new_value> for <field>
     And I click update resource
     Then I should see the <new_value> appears for <field>

     Examples:
     |field       |new_value  |
     |Name        |yourfile   |
     |Description |after      |
     |Type        |Code       |
     |Format      |json       |


   Scenario: Update Public dataset created by other should fail
     Given A public dataset was created by others
     And I am on dataset page
     Then I should not see Manage tab
     And I get an not authorized error if I try to enter the edit URL

