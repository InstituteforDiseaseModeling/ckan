import datetime

from ckan.common import _, config
from ckan.lib.helpers import date_str_to_datetime
from ckan.plugins.toolkit import Invalid

RANGE_MIN_DATE = date_str_to_datetime(config.get('ckan.range_min_date') or '1900-01-01')
RANGE_MAX_DATE = date_str_to_datetime(config.get('ckan.range_max_date') or '2100-01-01')
ACQ_MIN_DATE = date_str_to_datetime(config.get('ckan.acquisition_min_date')or '2010-01-01')
ACQ_MAX_DATE = date_str_to_datetime(config.get('ckan.acquisition_max_date')) if config.get('ckan.acquisition_max_date') else datetime.datetime.today()


def reasonable_range_date(value):
    _reasonable_date(value, RANGE_MIN_DATE, RANGE_MAX_DATE)

    return value


def reasonable_acquisition_date(value):
    _reasonable_date(value, ACQ_MIN_DATE, ACQ_MAX_DATE)

    return value


def temporal_range(key, data, errors, context):
    """Validates the start date is before the end date."""
    start_date = _get_date_value(data[('ext_startdate',)])
    end_date = _get_date_value(data[('ext_enddate',)])

    if start_date > end_date:
        raise Invalid(_('Start Date must be less or equal to End Date.'))

    return data[key]


def _reasonable_date(value, min_date, max_date):
    """Validates the date is in the given range."""
    value_date = _get_date_value(value)
    if value_date and value_date < min_date:
        raise Invalid(_('Must be higher or equal to {}'.format(min_date.date())))

    if value_date and value_date > max_date:
        raise Invalid(_('Must be less or equal to {}'.format(max_date.date())))


def _get_date_value(value):
    """Converts to datetime value if needed."""
    if  value is None or len(value.strip()) == 0:
        return None

    if isinstance(value, datetime.datetime):
        date_value = value
    if isinstance(value, str) or isinstance(value, unicode):
        date_value = date_str_to_datetime(value)
    else:
        raise Exception('Unsupported {} type.')

    return date_value
