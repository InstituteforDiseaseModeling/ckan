import configparser
import os

from dotenv import load_dotenv


load_dotenv(dotenv_path='.env')

volumes_dir = os.path.expanduser('~/ckan')
storage_path = os.path.normpath(os.path.join(volumes_dir, 'storage'))

ini_file_name = 'development.ini'
ini = configparser.RawConfigParser()
ini.read(ini_file_name)

ini['app:main']['ckan.storage_path'] = storage_path.replace(os.sep, '/')
ini['app:main']['sqlalchemy.url'] = 'postgresql://ckan:{}@localhost/ckan'.format(os.getenv('POSTGRES_PASSWORD'))
ini['app:main']['ckan.site_url'] = os.getenv('CKAN_SITE_URL')
ini['app:main']['solr_url'] = 'http://127.0.0.1:8983/solr/ckan/'


with open(ini_file_name, 'w') as ini_file:
    ini.write(ini_file)


