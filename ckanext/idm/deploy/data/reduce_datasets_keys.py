# TODO: Make this reusable script if this approach is used.
import json
import os

top_keys = [u'license_title', u'maintainer', u'request_access', u'acquisition_date', u'private', u'maintainer_email', u'spatial_gaps', u'quality', u'spatial_resolution', u'title', u'quality_notes', u'ext_enddate', u'version', u'location', u'spatial', u'license_id', u'type', u'resources', u'temporal_gaps', u'tags', u'spatial_mode', u'purpose', u'groups', u'ext_startdate', u'publisher', u'name', u'url', u'notes', u'owner_org', u'disease'] #, u'organization'
sub_keys = {
    u'resources': [u'mimetype', u'description', u'format', u'url', u'purpose', u'position', u'name'],
    u'groups': [u'name'],
    u'tags': [u'name']
}


def filter_list_of_dicts(d, target):
    return [{k: v for k, v in g.items() if k in sub_keys [target]} for g in d[target]]


here = os.path.abspath(os.path.dirname(__file__))
raw_dataset_path = os.path.join(here, u'import', u'datasets-data-services-raw.json')
dataset_path = os.path.join(here, u'import', u'datasets-data-services.json')

lines = []
with open(raw_dataset_path, u'rb') as f:
    for line in f.readlines():
        a = json.loads(line[:-1].decode(u"UTF-8"))
        b = {k: v for k, v in a.items() if k in top_keys}

        b[u'groups'] = filter_list_of_dicts(b, u'groups')
        b[u'tags'] = filter_list_of_dicts(b, u'tags')
        b[u'resources'] = filter_list_of_dicts(b, u'resources')
        b[u'owner_org'] = u'data_services'
        lines.append(json.dumps(b, ensure_ascii=False).encode(u"UTF-8") + '\n')

with open(dataset_path, u'wb') as fout:
    fout.writelines(lines)



# ckanapi commands

# ckanapi dump datasets --all -O datasets-data-services-raw.json -r http://localhost:5000 -a 9ac53be7-1dd9-4cd9-afa9-bbc374583e8a

# ckanapi dump datasets tamsat-v3 -O datasets-1.json -r http://localhost:5000 -a 9ac53be7-1dd9-4cd9-afa9-bbc374583e8a
# ckanapi dump datasets era5-daily-files -O datasets-2.json -r http://localhost:5000 -a 9ac53be7-1dd9-4cd9-afa9-bbc374583e8a
# ckanapi dump datasets era5-hourly-data -O datasets-3.json -r http://localhost:5000 -a 9ac53be7-1dd9-4cd9-afa9-bbc374583e8a

#  ckanapi load datasets -I data/import/datasets-data-services.json -a b2b9ca76-7a62-4a05-881a-aec2b6e911b9 -r http://localhost:5000

# Creating the list of keys from manually edited dataset.
#with open(r'C:\git\ckan\ckanext\idm\deploy\data\import\datasets-data-services-sample.json') as json_file:
#    sample = json.load(json_file)

#top_keys = sample.keys()
# sub_keys = {
#     'groups': sample['groups'][0].keys(),
#     'tags': sample['tags'][0].keys(),
#     'organization': sample['organization'].keys(),
#     'resources': sample['resources'][0].keys()
# }
#
# print sub_keys
