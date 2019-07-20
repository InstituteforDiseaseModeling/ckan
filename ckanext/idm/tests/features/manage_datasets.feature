@demo
@UI
Feature: Manage datasets
  Create, update and delete datasets

  Background:
    Given The use has registered
    Given The user is logged in
    Given The user is added to the research group

  Scenario: Create Data dataset with link and upload resource.
    Given I have the file
    Given I have dataset info
       | name  | description | url |
       | ERA5  | weather data| https://www.ecmwf.int/en/forecasts/datasets/reanalysis-datasets/era5|

    When I click "Add Dataset"
    Then I must set required dataset fields
      | fields            | values                          |
      | Title             | ERA5 daily files.               |
      | Description       | Daily files from ERA5 hourly.   |
      | Maintainer email  | dlukacevic@idmond.org           |
      | Type              | Data                            |
      | Research Group    | Data Services                   |
      | Disease           | Any                             |
      | Start Date        | 1979                            |
      | End Date          | 2018                            |
      | Country           | World                           |
      | Publisher         | IDM                             |
      | Acquisition Date  | 2019-03-01                      |
      | Version           | 1.0                             |
      | Visibility        | Public                          |
      | Restricted        | False                           |
      | License           | default                         |

    And I can set optional dataset fields
      | fields            | values                          |
      | Tags              | temperature rainfall humidity   |
      | Notes             | Quality: 1979-01-01 is bad      |
      | Topic             | Climate                         |
      | Origin URL        | https://wiki.idmod.org/display/SP/ERA5+Data+Sets  |

    And I can optionally add up to 3 fields with values
      | fields            | values                          |
      | Collaborator      | Mr.Smith                        |
      | Association       | UW                              |
      | ISO number        | 12345                           |

    And I can click "Add Data"

    And I can click "Link"
    And I must set required resource fields
      | fields            | values                          |
      | URL               | https://climate.copernicus.eu/climate-reanalysis |
      | Type              | Data                            |
      | Name              | ERA5 hourly                     |

    And I can set optional resource fields
      | fields            | values                          |
      | Description       | ERA5 hourly data for 1979-2018  |
      | Format            | netCDF                          |

    And I can click "Save & add another"

    And I can click "Upload" and select a local file
    And I must set required resource fields
      | fields            | values                          |
      | Type              | Origin                          |
      | Name              | Acquisition email               |

    And I can set optional resource fields
      | fields            | values                          |
      | Description       | When they told us about ERA5    |
      | Format            | email                           |

    And I can click "Finish"
