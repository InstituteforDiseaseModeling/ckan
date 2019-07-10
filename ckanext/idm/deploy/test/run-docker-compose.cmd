ECHO OFF
cd %~dp0

SET CKAN_TEST_RESULTS_OUT=%USERPROFILE%\ckan\test_results
IF NOT EXIST %CKAN_TEST_RESULTS_OUT% MKDIR %CKAN_TEST_RESULTS_OUT%

SET command=%1

IF "%command%"=="build" CALL :BUILD
IF "%command%"=="up"    CALL :UP
IF "%command%"=="down"  CALL :DOWN
IF "%command%"=="logs"  CALL :LOGS

IF "%command%"=="" (
  CALL :BUILD
  CALL :UP
  CALL :LOGS
  docker-compose down
  EXIT /B
)

GOTO :END

:BUILD
pushd ..
docker-compose build ckan
popd
docker-compose down
docker-compose build
EXIT /B

:UP
docker-compose down
DEL %CKAN_TEST_RESULTS_OUT%\*.* /Q
docker-compose up -d db-test solr-test redis-test datapusher-test
timeout 10
docker-compose up -d ckan-test
EXIT /B

:LOGS
docker-compose logs -f --tail=all ckan-test
EXIT /B

:DOWN
docker-compose down
EXIT /B

:END

ECHO ON
