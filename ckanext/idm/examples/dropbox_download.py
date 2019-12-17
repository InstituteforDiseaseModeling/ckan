# This example shows two possible scenarios:
# 1. Obtain dataset path to a local Dropbox dir.
# 2. Download dataset from Dropbox using API.
#
# Setup:
# - Install a new Python 2.7 virtual environment
# - pip install -r requirement.txt
# - Find Data Catalog API Key.
#       + In Data Catalog click on user name (top right).
#       + Look at the left bottom part of the page.
#       + For example, 11111111-2222-3333-4444-555566667777
# - Find Data Catalog dataset ID.
#       + In Data Catalog open the dataset page and find ID in the browser URL (last part).
#       + For example, in "http://data-catalog/dataset/pakistan-worldpop" dataset ID is "pakistan-worldpop".
# - Generate Dropbox authentication token (scenario 2 only):
#       + See instruction: https://www.iperiusbackup.net/en/create-dropbox-app-get-authentication-token/
#       + For example, xl_4444444444x4333_11111111117777777
#
# Run:
# - Usage:
#       python dropbox_download.py {Data Catalog API Key} {Data Catalog dataset ID} [--token {Dropbox authentication token}] [--dir-download]
# - For example (below guids are made-up):
#       python dropbox_download.py 11111111-2222-3333-4444-555566667777 pakistan-worldpop --token xl_4444444444x4333_11111111117777777


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
    #
    # YOUR CODE COULD GO HERE
    #

    if dropbox_token is None:
        return

    # Scenario 2a: Download a file from Dropbox
    dbx = dropbox.Dropbox(dropbox_token)
    download_path = tempfile.mkdtemp()
    scenario_2_download_file_from_dropbox(dbx, dropbox_path, download_path, u'licence.txt')
    print 'Downloaded file into {}'.format(download_path)
    #
    # YOUR CODE COULD GO HERE
    #

    # Scenario 2b: Download the entire dir from Dropbox
    if dir_download:
        metadata = scenario_2_download_dir_from_dropbox(dbx, dropbox_path, download_path)
        print 'Downloaded all files into {}'.format(download_path)
        print metadata
        #
        # YOUR CODE COULD GO HERE
        #


def get_dropbox_url_from_data_catalog(host_url, apikey, dataset_id):
    dc = RemoteCKAN(host_url, apikey=apikey)
    url = dc.action.package_show(id=dataset_id)['resources'][0]['url']
    dropbox_path = unquote(url.split(u'https://www.dropbox.com/home')[1])

    return dropbox_path


def scenario_1_local_dropbox_path(dropbox_path):
    dropbox_home_dir = os.path.join(os.path.expanduser("~"), 'Dropbox (IDM)')
    dropbox_local_path = os.path.normpath(dropbox_home_dir + str(dropbox_path))

    return dropbox_local_path


def scenario_2_download_file_from_dropbox(dbx, dropbox_path, download_path, file_name):
    download_file_path = os.path.join(download_path, file_name)
    dropbox_file_path = '{}/{}'.format(dropbox_path, file_name)
    dbx.files_download_to_file(download_file_path, dropbox_file_path)


def scenario_2_download_dir_from_dropbox(dbx, dropbox_path, download_dir_path):
    dir_name = '{}.zip'.format(os.path.basename(dropbox_path))
    download_path = os.path.join(download_dir_path, dir_name)
    metadata = dbx.files_download_zip_to_file(download_path, dropbox_path)

    return metadata


if __name__ == '__main__':
    example = 'python dropbox_download.py DATA-CATALOG_API_GUID DATASET_ID [--token DROPBOX_TOKEN_GUID] [--dir-download]'
    parser = argparse.ArgumentParser(example)

    parser.add_argument('apikey', default=None, help='Data Catalog API Key.')
    parser.add_argument('dataset_id', default='pakistan-worldpop', help='Data Catalog dataset ID. ')
    parser.add_argument('--token', dest='dropbox_token', default=None, help='Dropbox app authentication token. ')
    parser.add_argument('--dir-download', dest='dir_download', action='store_true', default=False, help='Download the entire dataset dir.')
    parser.add_argument('--host', dest='host_url', default='http://data-catalog', help='Data Catalog URL')


    args = parser.parse_args()
    main(args.host_url, args.apikey, args.dataset_id, args.dropbox_token, args.dir_download)

