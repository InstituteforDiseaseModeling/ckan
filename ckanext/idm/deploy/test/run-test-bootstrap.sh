#!/bin/bash
host=${1:-$(hostname)}
echo $host
pip install ckanapi
pip install pyyaml

user_request () {
  echo "check user: "$1
  echo "http --json GET http://"$2":5000/api/3/action/user_list q="$1
  json_result=$(http --json GET http://$2:5000/api/3/action/user_list q=$1)
  echo $json_result
  userid_result=$(echo $json_result | jq '.result[].id' | sed 's/"//g')
  if [ $3 -eq 0 ]; then echo "check new user is no longer there" && [ ! -z "$userid_result" ] && echo "Error: something wrong after restore" && exit 1; fi
  if [ $3 -eq 1 ]; then echo "check deleted user is back" && [ -z "$userid_result" ] && echo "Error: deleted user not recover restore" && exit 1; fi
}

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
bash volumes.sh backup test 2>&1 | tee /home/mewu/ckan/backup_$now.log
bash postgres.sh backup test 2>&1 | tee -a /home/mewu/ckan/backup_$now.log
backupfile=$(ls /mnt/ckan/backup/$HOSTNAME/test/ | grep 'docker_volumes')
backupfile="/mnt/ckan/backup/$HOSTNAME/test/"$backupfile
backupfile_sql=$(ls /mnt/ckan/backup/$HOSTNAME/test/ | grep 'postgres')
backupfile_sql="/mnt/ckan/backup/$HOSTNAME/test/"$backupfile_sql

#create new user
username=$(uuidgen -t)
echo "create user: "$username
echo "http --json POST http://"$host":5000/api/3/action/user_create name="$username" email=mewu@gmail.com password=12345678 Authorization:"$apikey
json=$(http --json POST http://$host:5000/api/3/action/user_create name=$username email=mewu@gmail.com password=12345678 Authorization:$apikey)
echo $json
userid=$(echo $json | jq '.result.id' | sed 's/"//g')
json_result=$(http --json GET http://$host:5000/api/3/action/user_list q=$username)
userid_result=$(echo $json_result | jq '.result[].id' | sed 's/"//g')
[ -z "$userid_result" ] && echo "Error: User creation failed before restore" && exit 1

#delete old user
echo "delete user: mewu"
echo "http --json POST http://"$host":5000/api/3/action/user_delete id=mewu Authorization:"$apikey
http --json POST http://$host:5000/api/3/action/user_delete id=mewu Authorization:$apikey
json_deleted=$(http --json GET http://$host:5000/api/3/action/user_list q=mewu)
echo $json_deleted
result_deleted=$(echo $json_deleted | jq '.result[].id' | sed 's/"//g')
[ ! -z "$userid_deleted" ] && echo "Error: User deletion failed before restore" && exit 1
#restore
echo "restore from backup: "$backupfile
echo "delete-all-data" | bash volumes.sh restore $backupfile  2>&1 | tee /home/mewu/ckan/restore_$now.log
sleep 10

user_request $username $host 0
user_request mewu $host 1

echo "restore from postgres backup: "$backupfile_sql
echo "delete-all-data" | bash postgres.sh restore $backupfile  2>&1 | tee -a /home/mewu/ckan/restore_$now.log
sleep 10

user_request $username $host 0
user_request mewu $host 1