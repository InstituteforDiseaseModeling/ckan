ECHO OFF
cd %~dp0

SET CKAN_TEST_RESULTS_OUT=%USERPROFILE%\ckan\test_results
IF NOT EXIST %CKAN_TEST_RESULTS_OUT% MKDIR %CKAN_TEST_RESULTS_OUT%

SET command=%1
SET idm_test_only=%2
SET ckan_test_run=%3

IF NOT DEFINED command SET command=run
IF "%command%"=="debug" SET ckan_test_run=False
IF "%command%"=="debug" SET command=run
IF NOT DEFINED idm_test_only SET idm_test_only=True
IF NOT DEFINED ckan_test_run SET ckan_test_run=True

ECHO idm_test_only:%idm_test_only%
ECHO ckan_test_run:%ckan_test_run%
ECHO command:%command%

SET IDM_TEST_ONLY=%idm_test_only%
SET CKAN_TEST_RUN=%ckan_test_run%


IF "%command%"=="build" CALL :BUILD
IF "%command%"=="up"    CALL :UP
IF "%command%"=="down"  CALL :DOWN
IF "%command%"=="logs"  CALL :LOGS

IF "%command%"=="run" (
  CALL :BUILD
  CALL :UP
  CALL :LOGS
  ECHO Check %CKAN_TEST_RESULTS_OUT%\nose.log for test results
  docker-compose down
  EXIT /B
)

GOTO :END

:BUILD
pushd ..
docker-compose build ckan
popd
docker-compose down --rmi local -v
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
