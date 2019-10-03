import fnmatch
import os
import unittest
import xmlrunner
from datetime import datetime, timedelta
from ckanapi import RemoteCKAN


class SmokeTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.check_env(u'BACKUP_ROOT', u'\\\\rivendell\\ActiveDevelopmentProjects\\ckan\\backup')
        cls.check_env(u'USER_NAME')
        cls.check_env(u'HOST_URL')
        cls.host_name = cls.host_url[cls.host_url.index(u'//') + 2: cls.host_url.rindex(u':')]
        cls.check_env(u'API_KEY')
        setattr(cls, u'action', RemoteCKAN(cls.host_url, apikey=cls.api_key).action)

    @classmethod
    def check_env(cls, env, default=None):
        value = os.environ.get(env)
        if not default:
            assert value, u'{} environment variable needs to be set'.format(env)
        setattr(cls, env.lower(), value if value else default)
        print('{} : {}'.format(env, value if value else default))

    def test_get_package(self):
        packages = self.action.package_list()
        self.assertGreater(len(packages), 0)

    def test_get_topics(self):
        topics = self.action.group_list()
        self.assertGreaterEqual(len(topics), 12)

    def test_get_orgs(self):
        orgs = self.action.organization_list()
        self.assertGreaterEqual(len(orgs), 10)

    def test_get_users(self):
        users = self.action.user_list()
        self.assertGreaterEqual(len(users), 50)

    def test_update_profile(self):
        updated_about = u'tested {}'.format(datetime.now().strftime(u"%Y-%m-%d, %H:%M:%S"))
        current_user = self.action.user_list(q=self.user_name)
        print(u'update user profile: ', self.user_name)
        self.assertEqual(1, len(current_user))
        self.action.user_update(id=current_user[0][u'id'], email=current_user[0][u'email'], about=updated_about)
        updated_user = self.action.user_list(q=self.user_name)
        self.assertEqual(updated_about, str(self.action.user_list(q=self.user_name)[0][u'about']))

    @unittest.skip(u'not yet implemented')
    def test_backup_status(self):
        backup_path = os.path.join(self.backup_root, self.host_name)
        pattern = u'postgres*.tar.gz'
        files = [os.path.join(backup_path, file) for file in os.listdir(backup_path)
                 if (fnmatch.fnmatch(file, pattern))]
        self.assertGreater(len(files), 0, u'no backup found!')
        files.sort(key=os.path.getmtime)
        lasthour_timestamp = datetime.now() + timedelta(hours=-1)
        created_timestamp = datetime.fromtimestamp(os.path.getmtime(files[-1]))
        print(u"last backup created at ",  created_timestamp.strftime(u"%Y-%m-%d, %H:%M:%S"))
        self.assertGreater(created_timestamp, lasthour_timestamp)


if __name__ == '__main__':
    if not os.path.exists(u'log'):
        os.makedirs(u'log')
    with open(os.path.join(os.path.curdir, 'log/ops_tests.xml'), 'wb') as output:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=output,
                                               failfast=False, verbosity=2, buffer=False))
