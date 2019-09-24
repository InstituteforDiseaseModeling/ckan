#!/bin/bash
cd /home/mewu/ckan/ckan
git reset --hard
git pull --rebase
cd ckanext/idm/deploy
docker-compose down -v
chmod +x deploy.sh
now=$(date +"%m_%d_%Y")
./deploy.sh prod 2>&1 | tee -a /home/mewu/ckan/deploy_$now.log
cd test
./run-test-bootstrap.sh
