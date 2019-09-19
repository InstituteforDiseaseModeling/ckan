import configparser
import os
import sys

from dotenv import load_dotenv

env_path = sys.argv[1]
ini_file_name = sys.argv[2]

load_dotenv(dotenv_path=env_path)

volumes_dir = os.path.expanduser(u'~/ckan')
storage_path = os.path.normpath(os.path.join(volumes_dir, u'storage'))

ini = configparser.RawConfigParser()
ini.read(ini_file_name)

ini[u'app:main'][u'ckan.storage_path'] = storage_path.replace(os.sep, u'/')
ini[u'app:main'][u'sqlalchemy.url'] = u'postgresql://ckan:{}@localhost/ckan'.format(os.getenv(u'POSTGRES_PASSWORD'))
ini[u'app:main'][u'ckan.site_url'] = os.getenv(u'CKAN_SITE_URL')
ini[u'app:main'][u'ckan.plugins'] = os.environ.get(u'CKAN_PLUGINS')
ini[u'app:main'][u'solr_url'] = u'http://127.0.0.1:8983/solr/ckan/'

ini[u'app:main'][u'scheming.dataset_schemas'] = u'ckanext.idm:schema.yml'
ini[u'app:main'][u'scheming.presets'] = u'ckanext.idm:presets.json'
ini[u'app:main'][u'scheming.dataset_fallback'] = u'false'

ini[u'app:main'][u'ckan.spatial.srid'] = u'4326'

with open(ini_file_name, u'w') as ini_file:
    ini.write(ini_file)


