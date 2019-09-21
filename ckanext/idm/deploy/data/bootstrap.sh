#!/usr/bin/env bash

paster user add dlukacevic email=dlukacevic@idmod.org fullname="Dejan Lukacevic" password=Password123 -c /etc/ckan/production.ini
paster sysadmin add dlukacevic -c /etc/ckan/production.ini
apikey=$(paster user dlukacevic -c /etc/ckan/production.ini | sed -n 's/<.*apikey=\([[a-zA-Z0-9-]*\)[[:space:]].*/\1/p')
echo $apikey
cd /home/ckan/src/ckan/ckanext/idm/deploy/data
python bootstrap.py $apikey
cd /home/ckan/src/ckan
