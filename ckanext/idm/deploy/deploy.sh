#!/usr/bin/env bash

export CKAN_SITE_URL=http://$HOSTNAME:5000

case  $1  in
      stage)
            echo "Deploying STAGE environment"
            docker-compose -f docker-compose.yml -f docker-local.yml build
            docker-compose -f docker-compose.yml -f docker-local.yml down
            docker-compose -f docker-compose.yml -f docker-local.yml up -d
            sleep 10
            docker-compose -f docker-compose.yml -f docker-local.yml up -d ckan
            docker-compose -f docker-compose.yml -f docker-local.yml logs
            ;;
      prod)
            echo "Deploying PROD environment"

            docker-compose build
            docker-compose down
            docker-compose up -d
            sleep 10
            docker-compose up -d ckan
            docker-compose logs
            ;;
      *)
esac
