import configparser
import os
import sys

from dotenv import load_dotenv

env_path = sys.argv[1]
ini_file_name = sys.argv[2]

load_dotenv(dotenv_path=env_path)

volumes_dir = os.path.expanduser('~/ckan')
storage_path = os.path.normpath(os.path.join(volumes_dir, 'storage'))

ini = configparser.RawConfigParser()
ini.read(ini_file_name)

ini['app:main']['ckan.storage_path'] = storage_path.replace(os.sep, '/')
ini['app:main']['sqlalchemy.url'] = 'postgresql://ckan:{}@localhost/ckan'.format(os.getenv('POSTGRES_PASSWORD'))
ini['app:main']['ckan.site_url'] = os.getenv('CKAN_SITE_URL')
ini['app:main']['ckan.plugins'] = os.environ.get('CKAN_PLUGINS')
ini['app:main']['solr_url'] = 'http://127.0.0.1:8983/solr/ckan/'

ini['app:main']['scheming.dataset_schemas'] = 'ckanext.idm:schema.yml'
ini['app:main']['scheming.presets'] = 'ckanext.idm:presets.json'
ini['app:main']['scheming.dataset_fallback'] = 'false'

ini['app:main']['ckan.spatial.srid'] = '4326'

with open(ini_file_name, 'w') as ini_file:
    ini.write(ini_file)


