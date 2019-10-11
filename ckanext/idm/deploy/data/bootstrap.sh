#!/usr/bin/env bash

paster user add dlukacevic email=dlukacevic@idmod.org fullname="Dejan Lukacevic" password=Password123 -c /etc/ckan/production.ini
paster sysadmin add dlukacevic -c /etc/ckan/production.ini
paster user remove default -c /etc/ckan/production.ini
apikey=$(paster user dlukacevic -c /etc/ckan/production.ini | sed -n 's/<.*apikey=\([[a-zA-Z0-9-]*\)[[:space:]].*/\1/p')
echo $apikey
cd /home/ckan/src/ckan/ckanext/idm/deploy/data
sleep 5
python bootstrap.py $apikey
sleep 20
python import.py $apikey import/dataset-fields-map-Caitlin.yaml import/datasets-Caitlin.csv
cd /home/ckan/src/ckan
