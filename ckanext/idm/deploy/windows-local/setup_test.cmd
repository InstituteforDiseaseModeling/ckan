REM This script sets up test environment

REM install dev dependencies
pip install -r ../../dev-requirements.txt
pip install -r ../../requirement-setuptools.txt
pip install -r test-requirements.txt
cd ../../
python setup.py develop

REM Create test db and users
docker exec -it db adduser --disabled-password --gecos "" ckan
docker exec -it db runuser -l ckan -c "psql -c \"CREATE USER ckan_default WITH PASSWORD 'pass' NOSUPERUSER NOCREATEDB NOCREATEROLE;\""
docker exec -it db runuser -l ckan -c "createdb -O ckan_default ckan_test -E utf-8"

REM Create datastore db users
docker exec -it db runuser -l ckan -c "psql -c \"CREATE USER datastore_read WITH PASSWORD 'pass' NOSUPERUSER NOCREATEDB NOCREATEROLE;\""
docker exec -it db runuser -l ckan -c "psql -c \"CREATE USER datastore_write WITH PASSWORD 'pass' NOSUPERUSER NOCREATEDB NOCREATEROLE;\""
docker exec -it db runuser -l ckan -c "createdb -O ckan_default datastore_test -E utf-8"

cd contrib/windows-local
REM initialize db and set permission
paster datastore set-permissions -c test-core.ini > testscript.txt
docker cp testscript.txt db:/tmp/testscript.txt
docker exec -it db runuser -l ckan -c "psql -f /tmp/testscript.txt"
paster db init -c test-core.ini

START paster serve test-core.ini
TIMEOUT 10

REM install npm packages and run ui tests
START /wait CMD /c npm install -g mocha-phantomjs@3.5.0 phantomjs@~1.9.1 mocha-xunit-reporter
CALL mocha-phantomjs http://localhost:5000/base/test/index.html -R xunit>test_mocha.xml

cd ../../
nosetests -v --ckan --ckan-migration --reset-db  --with-pylons=contrib/windows-local/test-core.ini --with-coverage --cover-package=ckan --cover-package=ckanext --with-xunit --xunit-file=ckan_test.xml ckan ckanext
ECHO if you want to run individual tests add --tests for example: --tests=TestAppDispatcher.test_ask_around_flask_core_and_pylons_extension_route
ECHO add --with-html --html-report=test.html for better reporting

PAUSE
REM stop web server (todo: find a better way to do it)
taskkill /IM python.exe /F


TIMEOUT 10
REM cleanup 
docker exec -it db runuser -l ckan -c "psql -c \"REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM datastore_read;\""
docker exec -it db runuser -l ckan -c "psql -c \"REVOKE ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public FROM datastore_read;\""
docker exec -it db runuser -l ckan -c "psql -c \"REVOKE ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public FROM datastore_read;\""
docker exec -it db runuser -l ckan -c "psql -c \"REVOKE USAGE ON SCHEMA public FROM datastore_read;\""
docker exec -it db runuser -l ckan -c "psql -c \"DROP USER datastore_read;\""


docker exec -it db runuser -l ckan -c "psql -c \"REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM datastore_write;\""
docker exec -it db runuser -l ckan -c "psql -c \"REVOKE ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public FROM datastore_write;\""
docker exec -it db runuser -l ckan -c "psql -c \"REVOKE ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public FROM datastore_write;\""
docker exec -it db runuser -l ckan -c "psql -c \"REVOKE USAGE ON SCHEMA public FROM datastore_write;\""
docker exec -it db runuser -l ckan -c "psql -c \"DROP USER datastore_write;\""

docker exec -it db runuser -l ckan -c "dropdb ckan_test"
docker exec -it db runuser -l ckan -c "dropdb datastore_test"

cd contrib/windows-local
START paster serve development.ini
