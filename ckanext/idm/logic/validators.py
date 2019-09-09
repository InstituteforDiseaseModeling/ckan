import datetime

from ckan.common import _, config
from ckan.lib.helpers import date_str_to_datetime
from ckan.plugins.toolkit import Invalid

MIN_DATE = date_str_to_datetime(config.get('ckan.min_date') or '1900-01-01')
MAX_DATE = date_str_to_datetime(config.get('ckan.max_date')) if config.get('ckan.max_date') else datetime.datetime.today()


def reasonable_date(value):
    value_date = _get_date_value(value)
    if value_date < MIN_DATE:
        raise Invalid(_('Must be higher or equal to {}'.format(MIN_DATE.date())))

    if value_date > MAX_DATE:
        raise Invalid(_('Must be less or equal to {}'.format(MAX_DATE.date())))

    return value


def temporal_range(key, data, errors, context):
    start_date = _get_date_value(data[('ext_startdate',)])
    end_date = _get_date_value(data[('ext_enddate',)])

    if start_date > end_date:
        raise Invalid(_('Start Date must be less or equal to End Date.'))

    return data[key]


def _get_date_value(value):
    if value is None:
        return None

    if isinstance(value, datetime.datetime):
        date_value = value
    if isinstance(value, str) or isinstance(value, unicode):
        date_value = date_str_to_datetime(value)
    else:
        raise Exception('Unsupported {} type.')

    return date_value
