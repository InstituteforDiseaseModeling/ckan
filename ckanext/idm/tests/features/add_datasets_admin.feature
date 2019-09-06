@demo
@UI
Feature: Manage datasets for admins
  #Create, update and delete datasets
  # Refer to https://wiki.idmod.org/display/SP/Phase+1%3A+Data+Catalog+Prototype
  Background:
    Given I am admin
    And I am logged in

  @allRequiredFields
  Scenario Outline: Research Group
    #all required fields as shown in the table
    Given I am ready to create dataset (tag:addDataset)
    Then I can set <Research Group> field
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
