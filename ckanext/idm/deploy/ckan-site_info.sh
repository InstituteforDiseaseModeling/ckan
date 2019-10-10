#!/bin/bash

paster config-tool $1 ckan.site_title="IDM Data Catalog"
paster config-tool $1 ckan.site_logo=/images/idm-logo.png
# favicon setting doesn't appear to work for uelrs which are not root
#paster config-tool $1 ckan.favicon=/images/idm-favicon.ico
