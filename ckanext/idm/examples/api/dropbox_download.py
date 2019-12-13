# This example shows two possible scenarios for integrating Data Catalog into research workflows:
# 1. Obtain dataset Dropbox path and convert it to a local path where Dropbox app is syncing files.
# 2. Obtain dataset Dropbox path and use Dropbox API to download data from Dropbox.
#
# Setup:
# - Install a new Python 2.7 virtual environment
# - pip install -r requirement.txt
# - Find Data Catalog API key. In Data Catalog click on user name (top right). Look at the left bottom part of the page.
# - Find Data Catalog dataset ID. In Data Catalog open the dataset page and find ID in the browser URL (last part).
# - For scenario 2 (Dropbox API) generate Dropbox authentication token. For instruction see:
#   https://www.iperiusbackup.net/en/create-dropbox-app-get-authentication-token/
#
# Run:
# - Run like this (below guids are made-up):
#   python dropbox_download.py 11111111-2222-3333-4444-555566667777 pakistan-worldpop --token xl_4444444444x4333_11111111117777777


import argparse
import dropbox
import os
import tempfile

from urllib import unquote
from ckanapi import RemoteCKAN


def main(host_url, apikey, dataset_id, dropbox_token, dir_download):
    print 'Connecting to {} '.format(host_url)
    dropbox_path = get_dropbox_url_from_data_catalog(host_url, apikey, dataset_id)
    print 'Dropbox path is {}'.format(dropbox_path)

    # Scenario 1: Construct local Dropbox path
    dropbox_local_path = scenario_1_local_dropbox_path(dropbox_path)
    print 'Local Dropbox dir is {}'.format(dropbox_local_path)


    if dropbox_token is None:
        return

    # Scenario 2a: Download a file from Dropbox
    dbx = dropbox.Dropbox(dropbox_token)
    download_path = tempfile.mkdtemp()
    scenario_2_download_file_from_dropbox(dropbox_path, dbx, download_path, u'licence.txt')
    print 'Downloaded file into {}'.format(download_path)

    # Scenario 2b: Download the entire dir from Dropbox
    if dir_download:
        metadata = scenario_2_download_dir_from_dropbox(dataset_id, dropbox_path, dbx, download_path)
        print 'Downloaded all files into {}'.format(download_path)
        print metadata


def get_dropbox_url_from_data_catalog(host_url, apikey, dataset_id):
    dc = RemoteCKAN(host_url, apikey=apikey)
    url = dc.action.package_show(id=dataset_id)['resources'][0]['url']
    dropbox_path = unquote(url.split(u'https://www.dropbox.com/home')[1])

    return dropbox_path


def scenario_1_local_dropbox_path(dropbox_path):
    dropbox_home_dir = os.path.join(os.path.expanduser("~"), 'Dropbox (IDM)')
    dropbox_local_path = os.path.normpath(dropbox_home_dir + str(dropbox_path))

    return dropbox_local_path


def scenario_2_download_file_from_dropbox(dropbox_path, dbx, download_path, file_name):
    download_file_path = os.path.join(download_path, file_name)
    dropbox_file_path = '{}/{}'.format(dropbox_path, file_name)
    dbx.files_download_to_file(download_file_path, dropbox_file_path)


def scenario_2_download_dir_from_dropbox(dropbox_path, dbx, download_path):
    metadata = dbx.files_download_zip_to_file(download_path, dropbox_path)

    return metadata


if __name__ == '__main__':
    example = 'python dropbox_download.py DATA-CATALOG_API_GUID DATA-CATALOG_DATASET_ID [--token DROPBOX_TOKEN_GUID] [--dir-download]'
    parser = argparse.ArgumentParser(example)

    parser.add_argument('apikey', default=None, help='Data Catalog API key.')
    parser.add_argument('dataset_id', default='pakistan-worldpop', help='Data Catalog dataset ID. ')
    parser.add_argument('--token', dest='dropbox_token', default=None, help='Dropbox app authentication token. ')
    parser.add_argument('--dir-download', dest='dir_download', action='store_true', default=False, help='Download the entire dataset dir.')
    parser.add_argument('--host', dest='host_url', default='http://data-catalog', help='Data Catalog URL')


    args = parser.parse_args()
    main(args.host_url, args.apikey, args.dataset_id, args.dropbox_token, args.dir_download)

