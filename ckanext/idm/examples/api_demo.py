import os

#https://github.com/ckan/ckanapi
from ckanapi import RemoteCKAN

host_url = u'http://localhost:5000'
api_key = u'9ac53be7-1dd9-4cd9-afa9-bbc374583e8a'
act = RemoteCKAN(host_url, apikey=api_key).action

# https://docs.ckan.org/en/2.8/api/

# http://localhost:5000/api/3/action/package_list
# http://localhost:5000/api/3/action/group_list
# http://localhost:5000/api/3/action/tag_list


tags = act.tag_list()
print 'Tags'
print os.linesep.join(tags[:2])
print ''

print u'Topics'
datasets = act.group_list()
print os.linesep.join(datasets[:2])
print ''


print u'Datasets'
datasets = act.package_list()
print os.linesep.join(datasets[:2], )
print ''

print 'Datasets & Resources'
datasets_resources = act.current_package_list_with_resources()
for dr in datasets_resources[:2]:
    print ''
    print os.linesep.join([str(d) for d in dr.items()])
print ''
