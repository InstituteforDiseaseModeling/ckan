ECHO OFF

REM This script sets up CKAN locally on Windows 10 to enable debugging from IDE.
REM This script uses docker containers to run depending compoents (all except the CKAN container).
REM This script mirrors the role of "ckanext/idm/deploy/ckan-entrypoint.sh" and includes some instructions from this Wiki:
REM https://github.com/ckan/ckan/wiki/How-to-Install-CKAN-2.5.2-on-Windows-7

REM Navigate to scripts dir (needed to be able to reference relative dirs).
pushd %~dp0

REM Apply needed ckan core chnages
xcopy source_change\after ..\..\..\.. /Y /S

REM Runs depending containers
CALL ..\run-docker-compose.cmd dev
timeout 10

REM Install required Python packages
pip install pip==9.0.1>nul 2>&1
pip install pip==9.0.1
pip install -r ..\..\..\..\requirement-setuptools.txt
pip install -r ..\..\..\..\requirements.txt
pip install -r ..\..\..\..\requirements-scheming.txt
pip install python-magic-bin==0.4.14 python-dotenv==0.10.3 configparser==3.7.4
pip install --upgrade bleach
pip install bin\Shapely-1.6.4.post2-cp27-cp27m-win_amd64.whl
pip install -r ..\..\..\..\requirements-spatial.txt

REM Creates config files
IF NOT EXIST who.ini copy  ..\..\..\..\ckan\config\who.ini who.ini
IF NOT EXIST development.ini (
  paster make-config --no-interactive ckan development.ini

  python populate_ini.py ..\.env development.ini
  REM TODO: refactor setting all config info
  ..\ckan-site_info.sh development.ini
)

REM Navigate to the ckan parent dir.
pushd ..\..\..\..\..

REM Initializes CKAN postgres db (requires installing and uninstalling CKAN python package).
pip install -e ckan

REM Setting this env. variable allows using "paster" commands without explicitly specifying config file.
SET CKAN_INI=%cd%\ckan\ckanext\idm\deploy\windows-local\development.ini
paster --plugin=ckan db init
paster --plugin=ckan spatial initdb

pip uninstall ckan -y

popd
popd

CALL start.cmd

ECHO ON
