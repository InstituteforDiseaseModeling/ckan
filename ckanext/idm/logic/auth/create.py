# encoding: utf-8

import ckan.authz as authz
import ckan.logic.auth as logic_auth

from ckan.common import _


def member_create(context, data_dict):
    group = logic_auth.get_group_object(context, data_dict)
    user = context[u'user']

    # User must be able to update the group to add a member to it
    permission = u'update'
    # However if the user is member of group then they can add/remove datasets
    if not group.is_organization and data_dict.get(u'object_type') == u'package':
        #permission = 'manage_group'

        # Allows any user to add any dataset to any topic.
        authorized = True
    else:
        authorized = authz.has_user_permission_for_group_or_org(group.id,
                                                                user,
                                                                permission)
    if not authorized:
        return {u'success': False,
                u'msg': _(u'User %s not authorized to edit group %s') %
                        (str(user), group.id)}
    else:
        return {u'success': True}
