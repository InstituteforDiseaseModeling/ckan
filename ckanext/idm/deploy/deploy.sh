#!/bin/bash

export CKAN_SITE_URL=http://$HOSTNAME:5000

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
    my_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
    cd $my_dir
    chmod +x deploy.sh
    chmod +x data/bootstrap.sh
}

function boot_data {
  docker exec ckan /home/ckan/src/ckan/ckanext/idm/deploy/data/bootstrap.sh
}

function deploy_prod {
  echo "Deploying PROD environment"
  docker-compose build
  docker-compose down
  docker-compose up -d
  sleep 10
  docker-compose up -d ckan
  docker-compose logs
  sleep 10
}

function deploy_stage {
  echo "Deploying STAGE environment"
  docker-compose -f docker-compose.yml -f docker-local.yml build
  docker-compose -f docker-compose.yml -f docker-local.yml down
  docker-compose -f docker-compose.yml -f docker-local.yml up -d
  sleep 10
  docker-compose -f docker-compose.yml -f docker-local.yml up -d ckan
  docker-compose -f docker-compose.yml -f docker-local.yml logs
  sleep 10
}

case  $1  in
      stage)
          deploy_stage
          ;;
      prod)
          deploy_prod
          ;;
      refresh-stage)
          git_pull
          deploy_stage
          ;;
      refresh-prod)
          git_pull
          deploy_stage
          ;;
      boot-stage)
          nuke
          git_pull
          deploy_stage
          boot_data
          ;;
      boot-prod)
          nuke
          git_pull
          deploy_stage
          boot_data
          ;;
      *)
esac
