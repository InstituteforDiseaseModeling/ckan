#!/bin/bash

export PYTHONPATH=$CKAN_HOME
export CKAN_TEST_RESULTS=/home/ckan/test_results

#Database setup

cd $CKAN_HOME
rm who.ini
cp $CKAN_HOME/ckan/config/who.ini .
cp $CKAN_HOME/ckanext/idm/deploy/test/test-core.ini .

export PGPASSWORD='ckan'

# Wait for PostgreSQL
while ! pg_isready -h db -U ckan; do
  sleep 1;
done

psql --host=db -U ckan -c "CREATE USER ckan_default WITH PASSWORD 'pass' NOSUPERUSER NOCREATEDB NOCREATEROLE;"
psql --host=db -U ckan -c "CREATE DATABASE ckan_test OWNER ckan_default;"
psql --host=db -U ckan -c "CREATE USER datastore_read WITH PASSWORD 'pass' NOSUPERUSER NOCREATEDB NOCREATEROLE;"
psql --host=db -U ckan -c "CREATE USER datastore_write WITH PASSWORD 'pass' NOSUPERUSER NOCREATEDB NOCREATEROLE;"
psql --host=db -U ckan -c "CREATE DATABASE datastore_test OWNER ckan_default;"

paster datastore -c test-core.ini set-permissions | psql --host=db -U ckan
paster db init -c test-core.ini

mkdir -p $CKAN_TEST_RESULTS
nohup paster serve test-core.ini 2>$CKAN_TEST_RESULTS/nohup.out &
jobs -l
cat $CKAN_TEST_RESULTS/nohup.out

if [[ $CKAN_TEST_RUN == "True" ]]; then
  sleep 5
  cd $CKAN_HOME/node_modules/mocha-phantomjs/bin/
  ./mocha-phantomjs -R xunit http://localhost:5000/base/test/index.html > $CKAN_TEST_RESULTS/result.log
  while read line; do echo $line | awk '/</{print $0}'; done < $CKAN_TEST_RESULTS/result.log > $CKAN_TEST_RESULTS/mocha-phantomjs.xml
  cat $CKAN_TEST_RESULTS/mocha-phantomjs.xml

  #start tests
  cd $CKAN_HOME
  nosetests --with-pylons=test-core.ini --version
  rm -f /home/ckan/results/junit.xml
  nosetests -v --ckan --reset-db --with-pylons=test-core.ini --nologcapture --with-coverage --cover-package=ckan --cover-package=ckanext --with-xunit --xunit-file=$CKAN_TEST_RESULTS/junit.xml $CKAN_TEST_1 $CKAN_TEST_2
  # --collect-only
else
    echo "noop"
    tail -F anything
fi







