#!/bin/bash
paster user add testadmin email=testadmin@idmod.org fullname="Test Admin" password="testPassword" -c /etc/ckan/production.ini
paster sysadmin add testadmin -c /etc/ckan/production.ini
apikey=$(paster user testadmin -c /etc/ckan/production.ini | sed -n 's/<.*apikey=\([[a-zA-Z0-9-]*\)[[:space:]].*/\1/p')
echo $apikey
echo $apikey > /home/ckan/src/ckan/ckanext/idm/deploy/data/apikey.txt