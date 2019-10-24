import os
import re
import sys
import yaml


def load_yaml(file_path):
    # TODO allow yaml to contain unicode
    with open(file_path, u'r') as stream:
        data = None
        data = yaml.safe_load(stream)

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
    return unicode(value, encoding=u'utf-8') if isinstance(value, str) else value

class ResearchGroupQueryHelper:
    def __init__(self, act):
        self.act = act
        self.research_groups = self._get_all_research_groups()
        self.research_group_id_name_map = {rg[u'id']: rg[u'name'] for rg in self.research_groups}

    def _get_all_research_groups(self):
        all_rg = call_api(self.act.organization_list, {u'all_fields': True, u'include_users': True})
        need_keys = [u'id', u'name', u'display_name']
        # all_research_groups = [_reduce_dict_keys(rg, need_keys) for rg in all_research_groups]
        all_rg_final = []
        for rg in all_rg:
            rg2 = _reduce_dict_keys(rg, need_keys)
            admins = [u[u'name'] for u in rg[u'users'] if u[u'capacity'] == u'admin']
            users = [u[u'name'] for u in rg[u'users'] if u[u'capacity'] != u'admin']
            rg2[u'admins'] = admins if len(admins) > 0 else None
            rg2[u'users'] = users
            all_rg_final.append(rg2)

        return all_rg_final

    def get_research_group(self, name, maintainer_email, exact=True, default=None):
        rgs = [g for g in self.research_groups if name == g[u'name']]
        if not exact and len(rgs) == 0:
            # TODO consider fuzzy matching
            rgs = [g for g in self.research_groups if name in g[u'name']]

        if (len(rgs) == 0 or rgs[0][u'name'] == default) and maintainer_email:
            maintainer = maintainer_email.split(u'@')[0]
            rgs = [g for g in self.research_groups if maintainer in self.get_all_users(g[u'name'])]

        if len(rgs) == 0 and default:
            rgs = [g for g in self.research_groups if default == g[u'name']]

        research_group = rgs[0] if len(rgs) > 0 else None

        return research_group

    def get_all_users(self, research_group=None, only_admin=False):
        all_users = []

        if research_group:
            rgs = [g for g in self.research_groups if g[u'name'] == research_group]
        else:
            rgs = self.research_groups

        for g in rgs:
            all_users.extend(g[u'admins'])
            if not only_admin:
                all_users.extend(g[u'users'])

        return all_users

    def get_research_group_admins(self, exclude_admins=None):
        if exclude_admins:
            rg_admins = {g[u'name']: [a for a in g[u'admins'] if not a in exclude_admins] for g in self.research_groups}
        else:
            rg_admins = {g[u'name']: g[u'admins'] for g in self.research_groups}

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


def extract_url(all_text):
    url = None
    if all_text:
        urls_re = re.search("(https?://[\w|\.|/|-|%]+)", all_text)
        if urls_re:
            urls = urls_re.groups()
            url = urls[0] if urls and len(urls) > 0 else None

    return url


def split_into_words(all_text):
    """
    Split text into words.
    https://stackoverflow.com/questions/12705293/regex-to-split-words-in-python
    """
    rgx = re.compile("(\w[\w']*\w|\w)")
    return rgx.findall(all_text)


def match_word(value, all_text, ignore_case=True):
    return re.search(ur'(?:\b|_){}(?=\b|_)'.format(value), all_text, flags=re.IGNORECASE if ignore_case else 0)


def get_ckan_port():
    port = os.environ[u'CKAN_PORT'] if u'CKAN_PORT' in os.environ else 5000

    return port


def research_groups_dropbox_dirs():
    dirs_dict = {
        u'measles': u'Measles Team Folder/Data',
        u'malaria': u'Malaria Team Folder/Data',
        u'dda': u'Data, Dynamics, and Analytics Folder/Data',
        u'stats': u'SMUG Folder'
    }

    return dirs_dict
