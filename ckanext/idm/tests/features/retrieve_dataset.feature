@demo
@UI
Feature: Retrieve dataset
  As a researcher,
  I want to use data catalog to search <keyword> by <field>
  so that I can find/download them

  Background:
    Given The user is logged in
    Given The user is added to the organization

  Scenario: retrieve the dataset url
    Given I know my dataset url
    When I enter url in the browser
    Then I can see my dataset page


  Scenario Outline: Search
    """
    We should agree on some fields that user can search on
    """
    When I type some <keyword> from a <field> that I know of
    Then I can find <document>

    Examples: IDM common fields
      | keyword                    |  field         | document|
      | Haiti malaria cases        |  Dataset Name  |   ?     |
      | cholera                    |  disease       |   ?     |
      | polio                      |  Research group|   ?     |
      | epidemic                   |  Paper         |   ?     |
      | genetic                    |  Tags          |   ?     |


  Scenario Outline: View file metadata
    When I find the dataset
    Then I can click the link to view values in metadata <field>

    Examples: IDM standard metadata
      | field       |
      | Author      |
      | Maintainer  |
      | Version     |
      | Last Updated|
      | Created     |


  Scenario: Download dataset
    Given that a dataset was previously uploaded
    When I find the dataset
    Then I can Click download and save a copy successfully


  Scenario Outline: Preview dataset
    Given the dataset was in the following <format>
    When I find the dataset
    Then I can preview it

    Examples:
      | format |
      | pdf    |
      | csv    |
      | txt    |
      | xlsx   |
      | png    |

