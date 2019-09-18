# encoding: utf-8
from ckan.logic.action import  create


def resource_create(context, data_dict):
    fields = ['name', 'url', 'description']
    has_data = any(len(data_dict[f]) > 0 for f in fields)

    if has_data:
        resource = create.resource_create(context, data_dict)
    else:
        resource = None

    return resource
