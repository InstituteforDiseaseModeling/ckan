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
# TODO: Use "--force" as a temp solution. This will be refactored in a more comprehensive import mechanism.
python import.py $apikey import/dataset-fields-map-Measles.yaml import/datasets-Measles.csv --force
ckanapi load datasets -I import/datasets-data-services.json -a $apikey -r http://localhost:${CKAN_PORT:-5000}
cd /home/ckan/src/ckan
