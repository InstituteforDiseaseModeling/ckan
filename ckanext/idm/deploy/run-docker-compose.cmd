ECHO OFF

pushd %~dp0
REM copy .dockerignore ..\..\..\.dockerignore
SET ts=%DATE:~-4%%DATE:~4,2%%DATE:~7,2%_%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%
SET ts=%ts: =0%

SET command=%1

IF "%command%"=="dev" (
  CALL :DOWN
  CALL :BUILD_BACKEND
  CALL :UP_BACKEND
)

IF "%command%"=="stage" (
  CALL :DOWN
  CALL :BUILD
  CALL :UP
)

IF "%command%"=="prod" (
  CALL docker-compose -f docker-compose.yml -f docker-local.yml down
  CALL docker-compose down
  CALL docker-compose build
  CALL docker-compose up -d
  CALL docker-compose logs -f --tail=5
)

IF "%command%"=="build"           CALL :BUILD
IF "%command%"=="build-backend"   CALL :BUILD_BACKEND
IF "%command%"=="build-ckan"      CALL :BUILD_CKAN
IF "%command%"=="down"            CALL :DOWN
IF "%command%"=="up"              CALL :UP
IF "%command%"=="up-backend"      CALL :UP_BACKEND
IF "%command%"=="up-ckan"         CALL :UP_CKAN
IF "%command%"=="logs"            CALL :LOGS %2
IF "%command%"=="backup"          CALL :BACKUP_VOLUMES
IF "%command%"=="boot"            CALL :BOOTSTRAP
IF "%command%"=="boot-stage"      CALL :BOOT_STAGE

GOTO :END

:BUILD
docker-compose -f docker-compose.yml -f docker-local.yml build
EXIT /B

:BUILD_CKAN
docker-compose -f docker-compose.yml -f docker-local.yml build ckan
EXIT /B

:UP
docker-compose -f docker-compose.yml -f docker-local.yml up -d
timeout 10
docker-compose -f docker-compose.yml -f docker-local.yml up -d ckan
EXIT /B

:DOWN
docker-compose -f docker-compose.yml -f docker-local.yml down
docker-compose -f docker-compose.yml -f docker-local.yml down
EXIT /B

:BUILD_BACKEND
docker-compose -f docker-compose.yml -f docker-local.yml build db solr redis
EXIT /B

:UP_BACKEND
docker-compose -f docker-compose.yml -f docker-local.yml up -d db solr redis
EXIT /B

:UP_CKAN
docker-compose -f docker-compose.yml -f docker-local.yml stop ckan
docker-compose -f docker-compose.yml -f docker-local.yml kill ckan
docker-compose -f docker-compose.yml -f docker-local.yml up -d ckan
EXIT /B

:LOGS
SET tail=%1
IF "%tail%"=="" SET tail=all
docker-compose -f docker-compose.yml -f docker-local.yml logs --tail=%tail%
EXIT /B

:EMPTY_CKAN_VOLUME
docker run --volumes-from ckan debian:stretch rm -r /var/lib/ckan/resources
docker run --volumes-from ckan debian:stretch rm -r /var/lib/ckan/storage
docker run --volumes-from ckan debian:stretch rm -r /var/lib/ckan/webassets
EXIT /B

:COPY_CKAN_LOCAL_TO_VOLUME
docker cp %USERPROFILE%\ckan\storage\resources ckan:/var/lib/ckan/resources
docker cp %USERPROFILE%\ckan\storage\storage ckan:/var/lib/ckan/storage
docker cp %USERPROFILE%\ckan\storage\webassets ckan:/var/lib/ckan/webassets
EXIT /B

:BACKUP_VOLUMES
CALL SET bk_dir=%USERPROFILE%\ckan\backup\%ts%
CALL mkdir %bk_dir%

docker cp ckan:/var/lib/ckan/resources %bk_dir%\ckan\resources
docker cp ckan:/var/lib/ckan/storage %bk_dir%\ckan\storage
docker cp ckan:/var/lib/ckan/webassets %bk_dir%\ckan\webassets
docker cp db:/var/lib/postgresql/data %bk_dir%\db
docker cp solr:/opt/solr/server/solr/ckan/data %bk_dir%\solr
EXIT /B

:BOOTSTRAP
docker exec ckan /home/ckan/src/ckan/ckanext/idm/deploy/data/bootstrap.sh
EXIT /B

:BOOT_STAGE
SET /P AREYOUSURE=Are you sure (Y/[N])?
IF /I "%AREYOUSURE%" NEQ "Y" GOTO :END

docker-compose down -v
CALL :DOWN
CALL :BUILD
CALL :UP
timeout 20
CALL :BOOTSTRAP
EXIT /B


:END
popd
REM popd
ECHO ON
