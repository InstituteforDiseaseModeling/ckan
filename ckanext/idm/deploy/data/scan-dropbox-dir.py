import argparse
import chardet
import codecs
import datetime
import helpers as hlp
import unicodecsv as csv
import os
import re
import tempfile
import urllib


def main(dropbox_dir, dropbox_url_prefix, output_path, filter_dir='', filter_file=''):

    with codecs.open(output_path, u'wb') as out_file:
        writer = init_writer(out_file)

        dir_fils_tuple_list = _get_all_files(dropbox_dir, exclude_dir=[dropbox_dir])

        for dir_path, file_name in dir_fils_tuple_list:

            exclude_dir_path = filter_dir and os.path.normpath(filter_dir) not in os.path.normpath(dir_path)
            exclude_file_name = filter_file and filter_file not in file_name

            if not u'README' in file_name or exclude_dir_path or exclude_file_name:
                continue

            relative_path, readme_path = get_dropbox_relative_path(dropbox_dir, dir_path, file_name)
            if not relative_path:
                print u'Skipping {}, empty relative path'.format(relative_path)
                continue

            parts = relative_path.split(os.sep)
            tags = topics = [parts[0]]

            location = parse_location(relative_path)
            title = u'{} {} {}'.format(location if location != u'Unknown' else '', topics[0], u' '.join(parts[2:])).strip()

            # Resources: construct dropbox url, set name to title and list of files to desc.
            resource_url = u'{}/{}'.format(dropbox_url_prefix, relative_path).replace(os.sep, u'/')
            resource_name = title
            resource_files = [f for d, f in dir_fils_tuple_list if d.startswith(dir_path) and f != file_name]
            resource_description_list = [u'Content:'] + resource_files[:10] + ['...' if len(resource_files) > 10 else '']
            resource_description = os.linesep.join(resource_description_list)

            # determine the encoding (provided by MeWu)
            with open(readme_path, u'rb') as f:
                raw_data = b''.join([f.readline() for _ in range(20)])
                encoding = chardet.detect(raw_data)[u'encoding']
                print(str(encoding))

            print u'{}, encoding: {}'.format(readme_path[len(dropbox_dir)+1:], encoding)

            with codecs.open(readme_path, u'rb', encoding=encoding) as readme_file:
                all_lines = readme_file.readlines()
                notes = os.linesep.join(all_lines)

                maintainer_email = resource_format = spatial_resolution = u''
                # Read README line by line and parse metadata
                for line in all_lines:
                    if not maintainer_email:
                        maintainer_email = parse_maintainer_email(line)

                    # if not resource_format:
                    #     resource_format = parse_resource_format(line, resource_files)

                    if not spatial_resolution:
                        spatial_resolution = parse_spatial_resolution(line)

                if not resource_format:
                    resource_format = parse_resource_files_format(resource_files)

            row = [title, notes, location, maintainer_email, spatial_resolution]
            row += [resource_url, resource_name, resource_format, resource_description]
            writer.writerow(row)


def init_writer(out_file):
    writer = csv.writer(out_file, encoding=u'utf-8', errors=u'replace')
    header = [u'title', u'notes', u'location', u'maintainer_email', u'spatial_resolution']
    header.extend([u'resource_url', u'resource_name', u'resource_format', u'resource_description'])
    writer.writerow(header)

    return writer


def get_dropbox_relative_path(dropbox_dir, dir_path, file_name):
    readme_path = os.path.join(dir_path, file_name)
    readme_path = os.path.normpath(readme_path)
    relative_path = dir_path[len(dropbox_dir) + 1:]

    return relative_path, readme_path


def parse_location(relative_path):
    parts = relative_path.split(os.sep)
    location = parts[1] if len(parts) >= 2 else u'Unknown'
    if location in location_aliases.keys():
        location = location_aliases[location]

    return location


def parse_maintainer_email(line):
    """Parse maintainer user name"""
    maintainer_email = u''
    if re.findall(u'[POC|Point of Contact].*:', line, flags=re.IGNORECASE):
        match = re.findall(u'\w+@idmod.org', line)
        if match:
            maintainer_email = match[0].split('@')[0]

    return maintainer_email


def parse_resource_format(line, resource_files):
    format_label = u'FORMAT:'
    resource_format = u''
    if format_label in line:
        resource_format = line.replace(format_label, '')

    return resource_format


def parse_resource_files_format(resource_files):
    resource_format = u''
    # extensions which need a more descriptive name
    names = {
        u'.dta': u'Stata',
        u'.tif': u'tiff',
        u'.xlsx': u'Microsoft Excel',
        u'.xls': u'Microsoft Access 2003',
        u'.docx': u'Microsoft Word',
        u'.doc': u'Microsoft Word 2003',
        u'.accdb': u'Microsoft Access',
        u'.mdb': u'Microsoft Access 2003',
        u'.pptx': u'Microsoft PowerPoint',
        u'.ppt': u'Microsoft PowerPoint 2003'
    }
    exts = names.keys() + [u'.tiff', u'.png', u'.csv', u'.shp', u'.pdf']

    for x in exts:
        if any([f.endswith(x) for f in resource_files]):
            resource_format = names[x] if x in names else x[1:]
            break

    return resource_format


def parse_spatial_resolution(line):
    spatial_resolution_label = u'SPATIAL RESOLUTION:'
    spatial_resolution = u''
    if spatial_resolution_label in line:
        spatial_resolution = line.replace(spatial_resolution_label, '')

    return spatial_resolution

def _parse_years_range(value):
    """Parse value and if years range is found, return them. Otherwise return None for both start and end years."""
    start_date = None
    end_date = None
    if value:
        years_regex = u'(19[0-9]{2}|20[0-9]{2}) *(-|\\|to) *(19[0-9]{2}|20[0-9]{2})'
        parts = re.findall(years_regex , value)
        if parts and isinstance(parts, list) and len(parts) > 0 and len(parts[0]) > 1:
            start_year = int(parts[0][0])
            end_year = int(parts[0][-1])

            start_date = datetime.datetime(start_year, 1, 1).strftime(u'%Y-%m-%d')
            end_date = datetime.datetime(end_year, 12, 31).strftime(u'%Y-%m-%d')

    return start_date, end_date


def _get_all_files(root_dir, exclude_dir=None):
    all_files = []
    for dir_path, _, files in os.walk(root_dir):
        if not exclude_dir or not dir_path in exclude_dir:
            all_files.extend([(dir_path, f) for f in files])

    return all_files

location_aliases = {
    u'DRC': u'Democratic Republic of the Congo',
    u'UK': u'United Kingdom'
}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(u'research_group')
    parser.add_argument(u'--url', dest=u'dropbox_root_url', default=os.path.normpath(u'https://www.dropbox.com/home/'))
    parser.add_argument(u'--dir', dest=u'dropbox_root_dir', default=None)

    parser.add_argument(u'--filter_dir', default='')
    parser.add_argument(u'--filter_file', default='')

    parser.add_argument(u'--output_path', default=None)

    return parser.parse_args()


if __name__ == u"__main__":
    args = parse_args()


    dropbox_data_dir = hlp.research_groups_dropbox_dirs()

    dropbox_root_dir = args.dropbox_root_dir or os.path.join(os.path.expanduser('~'), u'Dropbox (IDM)')
    dropbox_dir = os.path.normpath(os.path.join(dropbox_root_dir, dropbox_data_dir[args.research_group]))

    dropbox_url_prefix = u'{}/{}'.format(args.dropbox_root_url, urllib.quote(dropbox_data_dir[u'measles']))

    output_path = args.output_path or u'datasets-{}.csv'.format(args.research_group.title())

    main(dropbox_dir, dropbox_url_prefix, output_path, filter_dir=args.filter_dir, filter_file=args.filter_file)


