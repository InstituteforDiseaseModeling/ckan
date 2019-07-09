@demo
Feature: Site is up and running
  As a IT staff
  I want make sure the data catalog service is running

  Scenario: Data catalog components up and running
    Given The redis is up and running
    And The postgres database is up and running
    And The solr indexing is functioning
    Then The site should be up and running
