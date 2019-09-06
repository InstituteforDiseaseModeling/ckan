#!/bin/bash

export PYTHONPATH=$CKAN_HOME
export CKAN_TEST_RESULTS=/home/ckan/test_results

#Database setup

cd $CKAN_HOME
rm who.ini
cp $CKAN_HOME/ckan/config/who.ini .
cp $CKAN_HOME/ckanext/idm/deploy/test/test*.ini .

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
#psql --host=db -U ckan -d ckan_test -c 'CREATE EXTENSION postgis;'
#psql --host=db -U ckan -d ckan_test -c 'ALTER USER ckan_default WITH SUPERUSER;'

paster datastore -c test-core.ini set-permissions | psql --host=db -U ckan
paster db init -c test-core.ini

if [[ $CKAN_TEST_RUN == "True" ]]; then
  mkdir -p $CKAN_TEST_RESULTS
  TODO: see if "--daemon" could be used instead
  nohup paster serve test-core.ini 2>$CKAN_TEST_RESULTS/nohup.out &
  jobs -l
  cat $CKAN_TEST_RESULTS/nohup.out
  sleep 5
  cd $CKAN_HOME/node_modules/mocha-phantomjs/bin/
  ./mocha-phantomjs -R xunit http://localhost:5000/base/test/index.html > $CKAN_TEST_RESULTS/result.log
  while read line; do echo $line | awk '/</{print $0}'; done < $CKAN_TEST_RESULTS/result.log > $CKAN_TEST_RESULTS/mocha-phantomjs.xml
  cat $CKAN_TEST_RESULTS/mocha-phantomjs.xml

  #start tests
  cd $CKAN_HOME
  nosetests --with-pylons=test-core.ini --version
  echo "running "$CKAN_TEST
  echo "write result to nose.log"
  nosetests -v --ckan --reset-db --with-pylons=test-core.ini --nologcapture --with-coverage --cover-package=$CKAN_TEST  --ignore-files="test_coding_standards\.py" --with-xunit --xunit-file=$CKAN_TEST_RESULTS/ckan.xml $CKAN_TEST > $CKAN_TEST_RESULTS/nose.log 2>&1
  echo "running coding standard tests"
  nosetests -v --ckan --reset-db --with-pylons=test-core.ini --nologcapture --nocapture --with-xunit --xunit-file=$CKAN_TEST_RESULTS/ckan_coding_standard.xml ckan/tests/legacy/test_coding_standards.py ckan/tests/test_coding_standards.py >> $CKAN_TEST_RESULTS/nose.log 2>&1
  
  EXT_TEST=$(echo $EXT_TEST | tr -d '"')
  echo "running "$EXT_TEST
  nosetests -v --ckan --reset-db --with-pylons=test-core.ini --nologcapture --with-xunit --xunit-file=$CKAN_TEST_RESULTS/ckanext.xml $EXT_TEST >> $CKAN_TEST_RESULTS/nose.log 2>&1
  #added plugins
  paster --plugin=ckan spatial initdb -c test-core.ini
  nosetests -v --ckan --reset-db --with-pylons=test-idm.ini --nologcapture --with-coverage --cover-package=ckanext/idm --with-xunit --xunit-file=$CKAN_TEST_RESULTS/idm.xml ckanext/idm >> $CKAN_TEST_RESULTS/nose.log 2>&1
  #paster config-tool test-core.ini ckan.plugins="scheming_datasets scheming_groups scheming_organizations scheming_test_plugin"
  nosetests -v --ckan --reset-db --with-pylons=test-scheming.ini --nologcapture --with-coverage --cover-package=ckanext/scheming --with-xunit --xunit-file=$CKAN_TEST_RESULTS/scheming.xml ckanext/scheming >> $CKAN_TEST_RESULTS/nose.log 2>&1
  #paster config-tool test-core.ini ckan.plugins="test_spatial_plugin harvest spatial_metadata spatial_query spatial_harvest_metadata_api gemini_csw_harvester gemini_doc_harvester gemini_waf_harvester"
  nosetests -v --ckan --reset-db --with-pylons=test-spatial.ini --nologcapture --with-coverage --cover-package=ckanext/spatial --with-xunit --xunit-file=$CKAN_TEST_RESULTS/spatial.xml ckanext/spatial >> $CKAN_TEST_RESULTS/nose.log 2>&1
  
else
  sed -i "/^ckan.site_url.*=/s/=.*/= http:\/\/localhost:5000/" test-core.ini
  paster serve test-core.ini
  echo "noop"
  tail -F anything
fi

