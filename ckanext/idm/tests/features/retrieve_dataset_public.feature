@demo
@UI
Feature: Retrieve dataset for public access
  As a user not logged in,
  I want to use data catalog to search public dataset
  so that I can find/download them

  Background:
    Given I am logged out


  Scenario: retrieve the public dataset
    Given the visibility of the dataset is public
    When I go to the dataset page
    Then The dataset appears in the list


  Scenario: retrieve the private dataset
    Given the visibility of the dataset is private
    When I go to the dataset page
    Then The dataset does not appears in the list


  Scenario: Download public dataset
    Given the visibility of the dataset is public
    When I enter url in the browser
    Then I can Click download and save a copy successfully


  Scenario: Access private dataset
    Given the visibility of the dataset is private
    When I enter url in the browser
    Then I should receive "Dataset not found" error
