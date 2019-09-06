@demo
@UI
Feature: Update dataset
  As an admin, I can change the dataset created by others

  Background:
      Given I am admin
      And I am logged in

  Scenario Outline: Update Dataset metadata created by others
    Given A dataset was created by a non-admin user
    And I am on dataset page (tag:retrieveDataset)
    And I click "Manage"
    And I enter <new_values> in <fields>
    And I click "update dataset"
    Then I can see the dataset page with <new_values> in <fields>

     Examples:
     | fields            | values                                 |  new_values     |
     | Title             | ERA5 daily files.                      |  admin_ERA5     |
     | Description       | Daily files from ERA5 hourly.          |  admin_changed  |
     | Maintainer email  | dlukacevic@idmond.org                  |  admin@abc.com  |
     | Purpose           | Data                                   |  Paper          |
     | Quality Rating    | Good                                   |  Great          |
     | Quality Issues    | Unknown                                |  Passed         |
     | Research Group    | ECON                                   |  Malaria        |
     | Disease           | Any                                    |  Malaria        |
     | Start Date        | 1979/01/01                             |  1980/01/01     |
     | End Date          | 2018/12/31                             |  1980/01/02     |
     | Country           | World                                  |  USA            |
     | Publisher         | IDM                                    |  Unknown        |
     | Acquisition Date  | 2019/03/01                             |  2019/01/01     |
     | Version           | 1.0                                    |  2.0            |
     | Visibility        | Public                                 |  Private        |
     | Restricted        | False                                  |  True           |
     | License           | default                                |  Creative Commons Attribution  |
     | Temporal Gaps     | None                                   |  Missing Jan    |
     | Spatial Gaps      | None                                   |  TBD            |
     | Spatial Extent    | {"type":"Point","coordinates":[1, 30]} | {"type":"Point","coordinates":[2, 29]}  |



