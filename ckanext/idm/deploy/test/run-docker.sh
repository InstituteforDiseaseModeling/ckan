#!/bin/bash
cd "$(dirname "$0")"

export CKAN_TEST_RESULTS_OUT=~/ckan/test_results
mkdir -p $CKAN_TEST_RESULTS_OUT

cd ..
docker-compose down
docker-compose build ckan

cd test
docker-compose down
docker-compose build

rm -f $CKAN_TEST_RESULTS_OUT/*
docker-compose up -d db-test solr-test redis-test
sleep 10
docker-compose up -d ckan-test

docker-compose logs -f --tail=all ckan-test
