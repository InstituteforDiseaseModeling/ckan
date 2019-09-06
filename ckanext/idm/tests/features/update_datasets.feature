@demo
@UI
Feature: Update dataset
  As a researcher,
  I want to be able to update the dataset that was created previously
  This includes metadata and resources

 Background:
    Given I am logged in
    And I am added to the research group


 Scenario Outline: Update dataset metadata
   Given I have a dataset created with <values> for <fields>
   When I am on dataset page (tag:retrieveDataset)
   And I click "Manage"
   And I enter <new_values> in <fields>
   And I click "update dataset"
   Then I can see the dataset page with <new_values> in <fields>
   Examples:
     | fields            | values                                 |  new_values  |
     | Title             | ERA5 daily files.                      |  ERA5        |
     | Description       | Daily files from ERA5 hourly.          |  changed     |
     | Maintainer email  | dlukacevic@idmond.org                  |  xyz@abc.com |
     | Purpose           | Data                                   |  Paper       |
     | Quality Rating    | Good                                   |  Great       |
     | Quality Issues    | Unknown                                |  Passed      |
     | Disease           | Any                                    |  Malaria     |
     | Start Date        | 1979/01/01                             |  1980/01/01  |
     | End Date          | 2018/12/31                             |  1980/01/02  |
     | Country           | World                                  |  USA         |
     | Publisher         | IDM                                    |  Unknown     |
     | Acquisition Date  | 2019/03/01                             |  2019/01/01  |
     | Version           | 1.0                                    |  2.0         |
     | Visibility        | Public                                 |  Private     |
     | Restricted        | False                                  |  True        |
     | License           | default                                |  Creative Commons Attribution  |
     | Temporal Gaps     | None                                   |  Missing Jan |
     | Spatial Gaps      | None                                   |  TBD         |
     | Spatial Extent    | {"type":"Point","coordinates":[1, 30]} | {"type":"Point","coordinates":[2, 29]}  |


   Scenario: Change Topic Association
     Given the dataset is created and associated with a topic
     When I am on dataset page (tag:retrieveDataset)
     And I can change the topic association from the topic tab

   Scenario: Delete resource
     Given a dataset was previously created with resource uploaded
     When I am on the resource page
     And I click "Manage"
     Then I can delete the resource

   Scenario:  Add resource
     Given a dataset was previously created with resource uploaded
     When I am on dataset page (tag:retrieveDataset)
     And I click "Manage"
     And I go the "Edit Resource" tab and add a new resource
     Then I should see both old and new resources

   Scenario Outline: Edit resource metadata
     Given a dataset was previously created with resource uploaded
     And the resource has <old_value> appears for <field>
     When I am on the resource page
     And I click "Manage"
     And I change <new_value> for <field>
     And I click "update resource"
     Then I should see the <new_value> appears for <field>

     Examples:
     |field       |old_value  |new_value  |
     |Name        |myfile     |yourfile   |
     |Description |before     |after      |
     |Type        |Paper      |Code       |
     |Format      |csv        |json       |


   Scenario: Update Public dataset created by other should fail
     Given A public dataset was created by others
     And I am on dataset page (tag:retrieveDataset)
     Then I should not see "Manage" tab
     And I get an not authorized error if I try to enter the edit URL

