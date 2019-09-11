# encoding: utf-8

from ckanext.idm.logic.locations import get_location_geometry


def set_spatial_to_location_geometry(key, data, errors, context):
    location = data[('location',)]
    if data[('spatial_mode',)] != u'manual':
        data[('spatial',)] = get_location_geometry(location)

    return data[key]

