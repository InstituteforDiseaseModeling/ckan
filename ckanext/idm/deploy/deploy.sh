#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

export CKAN_SITE_URL=http://$HOSTNAME:5000

# Ensure working dir
OPS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $OPS_DIR

function nuke {
  read -p "Are you sure? "
  echo
  if [[ $REPLY =~ delete-all-data ]]
  then
    docker-compose down -v
  else
    exit 1
  fi

}

function git_pull {
    git fetch origin
    git reset --hard
    git clean -f
    git pull
    OPS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
    cd $OPS_DIR
    chmod +x deploy.sh
    chmod +x data/bootstrap.sh
}

function boot_data {
  docker exec ckan /home/ckan/src/ckan/ckanext/idm/deploy/data/bootstrap.sh
}

function setup_backup {
  bash ./ops/mount-backup-share.sh
  bash ./ops/create-backup-cron.sh
}

function deploy_prod {
  echo "Deploying PROD environment"
  docker-compose build
  docker-compose down
  prod_up
}

function deploy_stage {
  echo "Deploying STAGE environment"
  docker-compose -f docker-compose.yml -f docker-local.yml build
  docker-compose -f docker-compose.yml -f docker-local.yml down
  stage_up
}


function prod_up {
  docker-compose up -d
  sleep 10
  docker-compose up -d ckan
  docker exec ckan paster search-index rebuild -c /etc/ckan/production.ini
  docker-compose logs
  sleep 20
}

function stage_up {
  docker-compose -f docker-compose.yml -f docker-local.yml up -d
  sleep 10
  docker-compose -f docker-compose.yml -f docker-local.yml up -d ckan
  docker exec ckan paster search-index rebuild -c /etc/ckan/production.ini
  docker-compose -f docker-compose.yml -f docker-local.yml logs
  sleep 20
}


case  $1  in
      stage-up)
          stage_up
          ;;
      prod-up)
          prod_up
          ;;
      stage)
          deploy_stage
          ;;
      prod)
          deploy_prod
          ;;
      refresh-stage)
          git_pull
          deploy_stage
          setup_backup
          ;;
      refresh-prod)
          git_pull
          deploy_prod
          setup_backup
          ;;
      boot-stage)
          nuke
          git_pull
          deploy_stage
          boot_data
          setup_backup
          ;;
      boot-prod)
          nuke
          git_pull
          deploy_prod
          boot_data
          setup_backup
          ;;
      *)
esac
