@demo
@UI
Feature: Retrieve dataset
  As a researcher,
  I want to use data catalog to search <keyword> by <field>
  so that I can find/download them

  Background:
    Given I am logged in

  @retrieveDataset
  Scenario: retrieve the dataset url
    Given I know my dataset url
    When I enter url in the browser
    Then I can see my dataset page


  Scenario Outline: Search
    """
    We should agree on some fields that user can search on
    """
    Given the <document_title> is created with <keyword> in <field>
    When I type some <keyword> from a <field> in search box under dataset
    Then The <document_title>  appears in the list

    Examples: IDM common fields
      | keyword                    |  field           | document_title              |
      | uniqueTitleKeyword         |  Title           | test_search_title           |
      | uniqueDescKeyword          |  Description     | test_search_description     |
      | uniquemat@idmod.org        |  Maintainer      | test_search_maintainer      |
      | uniqueResearchGroup        |  Research group  | test_search_research_group  |
      | Measles                    |  Disease         | test_search_disease         |
      | uniqueTagVerySpecial       |  Tags            | test_search_tags            |
      | uniqueQualityIssuesNoNo    |  Quality Issues  | test_quality_rating         |
      | uniquePublisherIDM         |  Publisher       | test_publisher              |
      | uniqueOriginalURL          |  Origin Url      | test_origin_url             |


  Scenario: Global site search should return the same result as dataset search
    Given a dataset is created with "UniqueKeyword" in description
    When I type "UniqueKeyword" in the global search
    Then The result is the same as I type "UniqueKeyword" in the search box under dataset


  Scenario Outline: View dataset metadata
    Given I have created dataset with <field> filled with <value>
    And I am on dataset page (tag:retrieveDataset)
    Then I can click the link to view <value> in metadata <field>

    Examples: IDM standard metadata
      |field              |value          |
      |Maintainer         |mewu@idmod.org |
      |Purpose            |Raw Data       |
      |Disease            |Any            |
      |Quality Rating     |Good           |
      |Quality Issues     |N/A            |
      |Start Date         |2009-01-01     |
      |End Date           |2010-03-03     |
      |Temporal Gaps      |2010-12        |
      |Location           |Asia:Taiwan    |
      |Spatial Gaps       |Unknown        |
      |Spatial Extent     |{"type":"Point","coordinates":[116.0, 21]}|
      |Spatial Resolution |1km            |
      |Publisher          |SecretOrg      |
      |Origin URL         |www.idm.org    |
      |Acquisition Date   |1999-01-01     |
      |Version            |2a             |
      |Restricted         |Must request access from maintainer|
      |State              |active         |


  Scenario Outline: View resource metadata
    Given a dataset was previously created with resource uploaded
    When I am on dataset page (tag:retrieveDataset)
    And I can click the resource by its name and see the <field> in its properties

    Examples:
    | field       |
    | Name	      |
    | Description |
    | Type        |
    | Format      |

  @pri1
  Scenario: Download dataset
    Given a dataset was previously created with resource uploaded
    When I am on resource page
    Then I can Click download and save a copy successfully


  Scenario Outline: Preview dataset
    Given a dataset was previously created with resource uploaded
    And the resource was in the following <format>
    When I am on dataset page
    Then I can preview the resource

    Examples:
      | format |
      | json   |
      | txt    |
      | png    |

  @pri1
  Scenario Outline: Find Dataset by filters
    Given the dataset is created with metadata <filter>=<value>
    When I click Dataset
    Then I can find dataset by clicking <value> under <filter>

    Examples:
      | filter     | value        |
      | Location   | Asia:Taiwan  |
      | Disease    | HIV          |
      | Publisher  | SecretOrg    |
      | Formats    | json         |
      | Tags       | UniqueTag    |


  Scenario Outline: Find Dataset by Research Group
    Given the dataset is created with <Research Group>
    When I am on <Research Group> page
    Then I can see the dataset in the result list

    Examples:
    | Research Group  |
    | AMath           |
    | DDA             |
    | ECON            |
    | EPI             |
    | HAT             |
    | HIV             |
    | Malaria         |
    | Measles         |
    | MNCH            |
    | Polio           |
    | TB              |
    | Data Services   |


  Scenario: Find Dataset by Topic
    Given the dataset is created and associated with a topic
    When I am on topic page
    Then I can see the dataset in the result list


  Scenario Outline: Find Dataset by Temporal filter
    Given the dataset is created with <startdate> and <enddate>
    When I click Dataset
    And I enter <start> and <end> in the temporal filter
    Then dataset <return> if the range is within selection

    Examples:
      | stardate   | enddate     | start | end | return  |
      | 2009/01/01 | 2010/01/01  | 2009  | 2009| yes     |
      | 2009/01/01 | 2010/01/01  | 2009  | 2010| yes     |
      | 2009/01/01 | 2010/01/01  | 2009  | 2011| yes     |
      | 2009/01/01 | 2010/01/01  | 2008  | 2011| yes     |
      | 2009/01/01 | 2010/01/01  | 2011  | 2011| no      |


  @manualtesting
  Scenario: Find Dataset by Spatial filter
    Given the dataset is created with <location>
    When I click Dataset
    And I draw a rectangle area enclosed the <location>
    Then I can see the dataset found in the list
