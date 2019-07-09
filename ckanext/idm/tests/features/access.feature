@demo
@UI
Feature: User access story
  """
    manage common access use cases
  """
  Background:
    Given that I am a member of IDM


  Scenario: User can register
    When I click register
    And I enter my idmod email
    Then I can login after
    And ??? someone add me to org???


  Scenario: User register outside
     When I click register
     And I enter my other email
     Then ???


  Scenario: Admin management
    Given I am the admin of IDM organization
    And I click manage organization and add xx as a reader
    And I click manage organization and add yy as an admin
    Then xx should have read access
    And yy should have admin access


  Scenario: reset password
    Given I created an account
    When I click forgot my password
    Then I will receive email for resetting password

    


