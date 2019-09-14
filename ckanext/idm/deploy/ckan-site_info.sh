#!/usr/bin/env bash

paster config-tool $1 ckan.site_title="IDM Data Catalog"
paster config-tool $1 ckan.site_logo=images/idm-logo.png
