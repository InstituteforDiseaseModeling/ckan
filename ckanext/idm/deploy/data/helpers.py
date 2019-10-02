import sys
import yaml


def load_yaml(file_path):
    # TODO allow yaml to contain unicode
    with open(file_path, u'r') as stream:
        data = None
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print str(exc)

    return data


def call_api(func, args_dict={}, success_msg='', errors_to_skip=[]):
    u"""The common API call method handling exceptions used to detect existing data."""
    ok = True
    ret = None
    try:
        ret = func(**args_dict)
    except Exception as e:
        if u'NotAuthorized' in str(type(e)):
            print u"NotAuthorized: Make sure api key is valid and the user is a sysadmin."
            sys.exit(1)

        error_processed = False
        if len(errors_to_skip) > 0:
            ok = False
            for err_info in errors_to_skip:
                err = err_info[u'error']
                has_name_in_err_dict = hasattr(e, u'error_dict') and e.error_dict and e.error_dict.get(u'name')
                if has_name_in_err_dict and err in e.error_dict[u'name'][0] or err in str(e):
                    error_processed = True
                    print '{}: {}'.format(err_info[u'message'], str(e).strip())
                    break

        if not error_processed:
            raise e

    if ok and success_msg:
        print success_msg

    return ret


def _reduce_dict_keys(dc, need_keys):
    return {k: v for k, v in dc.items() if k in need_keys}

def to_unicode(value):
    return unicode(value, encoding='utf-8') if isinstance(value, str) else value

class ResearchGroupQueryHelper:
    def __init__(self, act):
        self.act = act
        self.research_groups = self._get_all_research_groups()
        self.research_group_id_name_map = {rg['id']: rg['name'] for rg in self.research_groups}

    def _get_all_research_groups(self):
        all_rg = call_api(self.act.organization_list, {u'all_fields': True, u'include_users': True})
        need_keys = [u'id', u'name', u'display_name']
        # all_research_groups = [_reduce_dict_keys(rg, need_keys) for rg in all_research_groups]
        all_rg_final = []
        for rg in all_rg:
            rg2 = _reduce_dict_keys(rg, need_keys)
            admins = [u['name'] for u in rg['users'] if u['capacity'] == 'admin']
            users = [u['name'] for u in rg['users'] if u['capacity'] != 'admin']
            rg2['admins'] = admins if len(admins) > 0 else None
            rg2['users'] = users
            all_rg_final.append(rg2)

        return all_rg_final


    def get_research_group(self, name, exact=True, default=None):
        rgs = [g for g in self.research_groups if name == g['name']]
        if not exact and len(rgs) == 0:
            # TODO consider fuzzy matching
            rgs = [g for g in self.research_groups if name in g['name']]

        if len(rgs) == 0 and default:
            rgs = [g for g in self.research_groups if default == g['name']]

        research_group = rgs[0] if len(rgs) > 0 else None

        return research_group

    def get_all_users(self, research_group=None, only_admin=False):
        all_users = []

        if research_group:
            rgs = [g for g in self.research_groups if g['name'] == research_group]
        else:
            rgs = self.research_groups

        for g in rgs:
            all_users.extend(g['admins'])
            if not only_admin:
                all_users.extend([g['users'] for g in self.research_groups])

        return all_users


    def get_research_group_admins(self, exclude_admins=None):
        if exclude_admins:
            rg_admins = {g['name']: [a for a in g['admins'] if not a in exclude_admins] for g in self.research_groups}
        else:
            rg_admins = {g['name']: g['admins'] for g in self.research_groups}

        return rg_admins


def fail_safe_check(force, func, label, max_count=0):
    # Fail safe, only run if DB is empty or unless "force" flag is used.
    if force:
        return

    cnt = len(func(all_fields=False))
    if cnt > max_count:
        print ImportError(u'Fail-safe: Found {} existing {}. This operation works only on an empty database. Use "--force" flag to override.'.format(cnt, label))
        sys.exit(1)


def report_errors(error_msg_list):
    if len(error_msg_list) > 1:
        for msg in error_msg_list:
            print u'  {}'.format(msg)


def take_word(all_text, start_str, new_start_str=None):
    if all_text and start_str and len(start_str) < len(all_text):
        the_rest = all_text.split(start_str)[1].split()[0]
        # checking explicitly for None so that '' is not ignored
        start = start_str if new_start_str is None else new_start_str
        word = '{}{}'.format(start, the_rest)
    else:
        word = None

    return word
