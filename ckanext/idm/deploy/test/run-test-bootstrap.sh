#!/bin/bash
host=${1:-$(hostname)}
echo $host
pip install ckanapi
pip install pyyaml

chmod +x create_apiuser.sh 
docker cp create_apiuser.sh ckan:/home/ckan/src/ckan/ckanext/idm/deploy/data/create_apiuser.sh

docker exec -i -w /home/ckan/src/ckan/ckanext/idm/deploy/data/ ckan /home/ckan/src/ckan/ckanext/idm/deploy/data/create_apiuser.sh

docker cp ckan:/home/ckan/src/ckan/ckanext/idm/deploy/data/apikey.txt ./apikey.txt

apikey=$(<apikey.txt)
echo "$apikey"

cd ../data/
python bootstrap.py $apikey --force
python bootstrap.py $apikey -f ../test/test_metadata.yml -p testPassword --force

