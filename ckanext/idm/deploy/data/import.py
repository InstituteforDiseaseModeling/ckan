# encoding: utf-8

import argparse
import codecs
import datetime
import re
import unicodecsv as csv

from ckanapi import RemoteCKAN

import helpers as hlp


def main():
    u""" """

    # Construct CKAN url and initiate API object.
    host_url = args.ckan_url or u'http://localhost:5000'
    act = RemoteCKAN(host_url, apikey=args.api_key).action
    rgh = hlp.ResearchGroupQueryHelper(act)

    hlp.fail_safe_check(args.force, act.package_list, 'datasets')

    # Get argument dict to be populated for each row and passed to API function
    ds_fields, rs_fields = get_args_dicts_from_schema()
    ds_fields_map, ds_defaults_map, resource_fields_maps = prep_field_column_maps(ds_fields, rs_fields)

    # Get dataset .csv file reader
    reader = get_dataset_file_reader(args.dataset_file)

    # Process .csv dataset file. Iterate over all lines
    header = None
    for row in reader:
        if not header:
            header = row
        else:
            # Convert line list into header-value dictionary
            row_dict = {header[i]: row[i] if i < len(row) else u'' for i in range(len(header))}

            # Track all encountered errors
            error_msgs = []

            # Populate fields dict with values from the .csv file row for datasets and resources
            ds_dict = populate_fields_from_row(row_dict, ds_fields, ds_fields_map, ds_defaults_map, error_msgs)
            prep_dataset_args(rgh, ds_dict, ds_defaults_map, error_msgs)
            populate_resources(rgh, row_dict, rs_fields, ds_dict, resource_fields_maps, error_msgs)

            # Call create dataset/resources API
            if ds_dict and len(error_msgs) == 0:
                # If field dict was populated call API to create the dataset (for that one .csv file row).
                api_create_dataset(act, ds_dict)
            else:
                # If there were errors, report them and skip this row.
                msg = error_msgs[0] if len(error_msgs) == 1 else u"unable to prepare dataset arguments"
                print u"Skipping dataset: {} for {}".format(msg, _message_postfix(ds_dict))
                hlp.report_errors(error_msgs)


def get_dataset_file_reader(dataset_file):
    with codecs.open(dataset_file, mode=u'rb', encoding=u'utf-8', errors=u'replace') as csvfile:
        # Read the file as unicode and parse as csv.
        lines = csvfile.readlines()

    lines_encoded = [x.encode(u'utf-8') for x in lines]
    reader = csv.reader(lines_encoded, encoding=u'utf-8', errors=u'replace')

    return reader


def prep_field_column_maps(ds_fields, rs_fields):
    # Lead field-column mapping: how dataset schema fields should be populated with columns from the .csv file.
    fields_columns_map = hlp.load_yaml(args.field_map_file)

    # Expand field-column dict with missing fields (per field list from schema)
    ds_fields_map, ds_defaults_map = get_full_fields_map(fields_columns_map[u'dataset'], ds_fields)

    resource_fields_maps = []
    for rs_fields_columns_map in fields_columns_map[u'resource']:
        rs_fields_map, rs_defaults_map = get_full_fields_map(rs_fields_columns_map, rs_fields)
        resource_fields_maps.append((rs_fields_map, rs_defaults_map))

    return ds_fields_map, ds_defaults_map, resource_fields_maps


def populate_resources(rgh, row_dict, rs_fields, ds_dict, resource_fields_maps, error_msgs):
    ds_dict['resources'] = []
    for rs_fields_map, rs_defaults_map in resource_fields_maps:
        rs_dicts = populate_fields_from_row(row_dict, rs_fields, rs_fields_map, rs_defaults_map, error_msgs)
        prep_resource_args(rgh, rs_dicts, rs_defaults_map, error_msgs)

        if any([v for (k, v) in rs_dicts.items() if k != 'purpose']):
            ds_dict['resources'].append(rs_dicts)


def get_full_fields_map(fields_columns_map, fields):
    fields_map = fields_columns_map[u'fields']
    defaults_map = fields_columns_map[u'defaults'] if u'defaults' in fields_columns_map else {}

    full_fields_map = {f: fields_map[f] if f in fields_map else None for f in fields}
    full_fields_defaults_map = {f: defaults_map [f] if f in defaults_map else '' for f in fields}

    return full_fields_map, full_fields_defaults_map


def get_full_resource_fields_map(rs_fields):
    fields_columns_map = hlp.load_yaml(args.field_map_file)
    fields_map = fields_columns_map[u'resource_fields']
    defaults_map = fields_columns_map[u'resource_defaults']

    full_fields_map = {f: fields_map[f] if f in fields_map else None for f in rs_fields}
    full_fields_defaults_map = {f: defaults_map[f] if f in defaults_map else None for f in rs_fields}

    return full_fields_map, full_fields_defaults_map


def get_args_dicts_from_schema():
    schema = hlp.load_yaml(u'../../schema.yml')
    ds_dict = [f[u'field_name'] for f in  schema[u'dataset_fields']]
    rs_dict = [f[u'field_name'] for f in  schema[u'resource_fields']]

    return ds_dict, rs_dict


def get_org_id(act, org):
    rg = hlp.call_api(act.organization_show, {u'id': org}) # 'all_fields': True
    return rg[u'id']


def get_maintainer(rgh, maintainer, research_group_id, default):
    user = maintainer
    research_group = rgh.research_group_id_name_map[research_group_id] if research_group_id else None
    if not maintainer in rgh.get_all_users():
        research_group_admins = rgh.get_research_group_admins(exclude_admins=[default])
        if research_group in research_group_admins.keys():
            user = research_group_admins[research_group][0]
        else:
            user = default

    try:
        user_ascii = user.encode(u"ascii")
    except UnicodeDecodeError as e:
        print e.message
        user_ascii = None

    return user_ascii


def populate_fields_from_row(row_dict, fields, fields_map, defaults_map, error_msgs):
    u""" Populate dataset/resource dictionary based on filed-column map.
        Read how fields should be populated (set into variable target).

        There are three options:
        1. fields_map gives the name of the column to be used
        or one or two to the below
        2. fields_map gives a string with parameters to be replaced with format
        3. fields_map gives a string to be eval.

        If field map .yaml doesn't specify mapping, the default is used. If the default is not specified '' is used.
    """
    args_dict = {}
    for field in fields:
        # Conventions in field-map file:
        eval_prefix = u'eval: '

        target = fields_map[field]
        value = None
        # Process field-column mapping if defined(specified in the target variable).
        if target:
            # Replace nameless params {} with []. They are reserved for the eval mode.
            target = target.replace(u'{}', u'[nameless]')
            # Determine the field-column mapping mode.
            has_params = u'{' in target and u'}' in target
            has_eval = target[:len(eval_prefix)] == eval_prefix
            if has_params or has_eval:
                # Replace params for value (relevant if there is no eval) and target (relevant for eval).
                target = value = target.format(**row_dict)
                if has_eval:
                    # Remove eval prefix
                    target = target[len(eval_prefix):]
                    try:
                        # Encode unicode chars to preserve them through eval.
                        target = target.encode(u'utf-8')
                        # Put back nameless params {} (if exist).
                        target = target.replace(u'[nameless]', u'{}')
                        value = eval(target)
                        # Put back unicode characters.
                        value = value.decode(u'utf-8')
                    except Exception as e:
                        error_msgs.append(('eval error: {}'.format(str(e))))
                        value = None
            else:
                # If target is a column name, read the value from the row dict.
                value = row_dict[target] if target else None

        if value:
            if len(value.replace(u'\n', u'').strip()) == 0:
                value = None
            else:
                value = value.strip()

        if not value:
            value = hlp.to_unicode(defaults_map[field])

        args_dict[field] = value

    return args_dict


def prep_dataset_args(rgh, ds_dict, ds_defaults_map, error_msgs):
    # transform to meet API expectation
    ds_dict[u'type'] = u'dataset'
    ds_dict[u'state'] = u'active'

    if ds_dict[u'request_access'] == u'True':
        ds_dict[u'request_access'] = u'maintainer'
    else:
        del ds_dict[u'request_access']

    if ds_dict[u'spatial_mode'] == u'True':
        ds_dict[u'spatial_mode'] = u'manual'
    else:
        del ds_dict[u'spatial_mode']

    ds_dict[u'tags'] = [{u'state': u'active', u'name': n} for n in ds_dict[u'tag_string'].split()]

    research_group = rgh.get_research_group(ds_dict[u'owner_org'], exact=False, default=ds_defaults_map[u'owner_org'])
    ds_dict[u'owner_org'] = _validate_args_dict_value(error_msgs, u'research group', research_group, 'id')

    maintainer_email = get_maintainer(rgh, ds_dict[u'maintainer_email'], ds_dict[u'owner_org'], ds_defaults_map[u'maintainer_email'])
    ds_dict[u'maintainer_email'] = _validate_args_dict_value(error_msgs, u'maintainer_email', maintainer_email)

    name = ds_dict[u'name']
    if name:
        name = ''.join([s for s in name if s.isalpha() or s.isnumeric() or s in [u'-', u'_', u' ']])
        name = name.encode("ascii", errors=u'replace')
        name = name.strip().lower().replace('  ', ' ').replace(' ', '-').replace(u'?', u'u')

    ds_dict[u'name'] = name

    if ds_dict['ext_startdate'] == '1900-01-01' and ds_dict['ext_enddate'] == '1900-01-01':
        start_year, end_year = _parse_years_range(ds_dict[u'title'])
        if start_year and end_year:
            ds_dict['ext_startdate'] = datetime.datetime(start_year, 1, 1).strftime('%Y-%m-%d')
            ds_dict['ext_enddate'] = datetime.datetime(end_year, 12, 31).strftime('%Y-%m-%d')


def prep_resource_args(rgh, rs_dict, rs_defaults_map, error_msgs):
    # if not rs_dict['url']:
    #     rs_dict['url'] = _parse_url(rs_dict['name'])
    #
    # if not rs_dict['url']:
    #     rs_dict['url'] = _parse_url(rs_dict['description'])

    # if not rs_dict['purpose']:
    #     rs_dict['purpose'] = 'data'
    pass


def _parse_years_range(value):
    start_year = None
    end_year = None
    if value:
        years_regex = '(19[0-9]{2}|20[0-9]{2}) *(-|\\|to) *(19[0-9]{2}|20[0-9]{2})'
        parts = re.findall(years_regex , value)
        if parts and isinstance(parts, list) and len(parts) > 0 and len(parts[0]) > 1:
            start_year = int(parts[0][0])
            end_year = int(parts[0][-1])

    return start_year, end_year


def _parse_url(value):
    url_maybe = ''
    if value:
        url_maybe = re.search("(?P<url>https?://[^\s]+.pdf|.html|.html)", value)
        if url_maybe:
            url_maybe = url_maybe.group("url")

    return  url_maybe


def _validate_args_dict_value(error_msgs, field, item, key=None):
    value = item[key] if item and key else item

    if value is None:
        error_msgs.append(u"Unable to determine {}".format(field))

    return value

def api_create_dataset(act, args_dict):
    success_msg = u'Created a new dataset {}'.format(args_dict[u'name'])
    errors_to_skip = [
        {
            u'error': u'That URL is already in use.',
            u'message': u'Dataset already exists: {}'.format(_message_postfix(args_dict))
        },
        {
            #u'error': u'Must be purely lowercase alphanumeric (ascii) characters and these symbols',
            u'error': u'maintainer_email',
            u'message': u'Skipping, maintainer is invalid: {}'.format(_message_postfix(args_dict))
        },
        {
            u'error': u'Enter a username, an email or a contact',
            u'message': u'Skipping, maintainer is invalid: {}'.format(_message_postfix(args_dict))
        },
        {
            u'error': u'Missing value',
            u'message': u'Skipping, missing a required field : {}'.format(_message_postfix(args_dict))
        }
    ]

    if not args.dryrun:
        hlp.call_api(act.package_create, args_dict, success_msg, errors_to_skip)


def _message_postfix(args_dict):
    value = '{} ({})'.format(args_dict[u'title'].encode(u'utf-8'), args_dict[u'name'].encode(u'utf-8'))
    value = unicode(value, encoding=u'utf-8', errors=u'replace')

    return value


def parse_args():
    example = ur"python import.py 0b7ba2a2-9d19-42da-a656-89937f856b4b import/dataset-fields-map-Caitlin.yaml import/datasets-Caitlin-2-rows.csv"
    parser = argparse.ArgumentParser(example)
    parser.add_argument(u'api_key')
    parser.add_argument(u'field_map_file')
    parser.add_argument(u'dataset_file')
    parser.add_argument(u'--url', dest=u'ckan_url', default=None)
    parser.add_argument(u'--dryrun', action=u'store_true')
    parser.add_argument(u'--force', action=u'store_true')
    return parser.parse_args()


if __name__ == u"__main__":
    args = parse_args()
    main()


