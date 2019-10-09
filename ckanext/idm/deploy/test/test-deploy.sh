#!/bin/bash
webhookurl=https://outlook.office.com/webhook/ecfa8776-a22c-414f-975a-c1735464c14a@7cae4d00-e099-4686-9873-ba27c351d11e/IncomingWebhook/2fb34f43a558470c9644a3ba77374281/a70235de-2b93-4ad1-9b26-b7520d7ec585
cd /home/mewu/ckan/ckan
git reset --hard
git pull --rebase
cd ckanext/idm/deploy
docker-compose down -v
chmod +x deploy.sh
now=$(date +"%m_%d_%Y")
rm -rf /mnt/ckan/test/deploy/*.*
./deploy.sh refresh-prod 2>&1 | tee /home/mewu/ckan/deploy_$now.log
cd test
chmod +x run-test-bootstrap.sh
./run-test-bootstrap.sh 2>&1 | tee /home/mewu/ckan/bootstrap_$now.log

yes | cp -rf /home/mewu/ckan/*_$now.log /mnt/ckan/test/deploy
logfile=file://P:/ckan/test/deploy

err_deploy=$(cat /home/mewu/ckan/deploy_$now.log | grep Error)
err_backup=$(cat /home/mewu/ckan/backup_$now.log | grep Error)
err_restore=$(cat /home/mewu/ckan/restore_$now.log | grep Error)
err_bootstrap=$(cat /home/mewu/ckan/bootstrap_$now.log | grep Error)

curl -H "Content-Type: application/json" -d "{\"text\": \"Deployed Finished: see logs in ${logfile}\n ERROR FROM Log:\n $err_deploy\"}" $webhookurl
curl -H "Content-Type: application/json" -d "{\"text\": \"Backup Finished: see logs in ${logfile}\n ERROR FROM Log:\n $err_backup\"}" $webhookurl
curl -H "Content-Type: application/json" -d "{\"text\": \"Restore Finished: see logs in ${logfile}\n ERROR FROM Log:\n $err_restore\"}" $webhookurl
curl -H "Content-Type: application/json" -d "{\"text\": \"Bootstrap Finished: see logs in ${logfile}\n ERROR FROM Log:\n $err_bootstrap\"}" $webhookurl
