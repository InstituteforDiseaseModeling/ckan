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
python bootstrap.py $apikey -f ../test/test_metadata.yaml -p testPassword --force

#import
docker exec -i -w /home/ckan/src/ckan/ckanext/idm/deploy/data/ ckan python import.py $apikey import/dataset-fields-map-Caitlin.yaml import/datasets-Caitlin.csv --force

#backup
echo "remove old backup"
rm -rf  /mnt/ckan/backup/$HOSTNAME/test/
cd ../ops
now=$(date +"%m_%d_%Y")
echo "create new backup"
bash volumes.sh backup test 2>&1 | tee -a /home/mewu/ckan/backup_$now.log
backupfile=$(ls /mnt/ckan/backup/$HOSTNAME/test/ | grep '.tar.gz')
backupfile="/mnt/ckan/backup/$HOSTNAME/test/"$backupfile

#create new user
username=$(uuidgen -t)
echo "create user: "$username
json=$(http --json POST http://$host:5000/api/3/action/user_create name=$username email=mewu@gmail.com password=12345678 Authorization:$apikey)
echo $json
userid=$(echo $json | jq '.result.id' | sed 's/"//g')
json_result=$(http --json GET http://$host:5000/api/3/action/user_list q=$username)
userid_result=$(echo $json_result | jq '.result[].id' | sed 's/"//g')
[ -z "$userid_result" ] && echo "Error: User creation failed before restore" && exit 1

#delete old user
echo "delete user: mewu"
http --json POST http://$host:5000/api/3/action/user_delete id=mewu Authorization:$apikey
json_deleted=$(http --json GET http://$host:5000/api/3/action/user_list q=mewu)
echo $json_deleted
result_deleted=$(echo $json_deleted | jq '.result[].id' | sed 's/"//g')
[ ! -z "$userid_deleted" ] && echo "Error: User deletion failed before restore" && exit 1
#restore
echo "restore from backup: "$backupfile
echo "delete-all-data" | bash volumes.sh restore $backupfile  2>&1 | tee -a /home/mewu/ckan/restore_$now.log

#check new user is no longer there
echo "check user: "$username
json_result=$(http --json GET http://$host:5000/api/3/action/user_list q=$username)
echo $json_result
userid_result=$(echo $json_result | jq '.result[].id' | sed 's/"//g')
[ ! -z "$userid_result" ] && echo "Error: something wrong after restore" && exit 1

#check deleted user is back
echo "check user: mewu"
json_deleted=$(http --json GET http://$host:5000/api/3/action/user_list q=mewu)
echo $json_deleted
result_deleted=$(echo $json_deleted | jq '.result[].id' | sed 's/"//g')
[ -z "result_deleted" ] && echo "Error: deleted user not recover restore" && exit 1