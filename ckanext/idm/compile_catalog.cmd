pushd %~dp0\..\..
python setup.py compile_catalog --directory ckanext\idm\i18n --locale en
popd