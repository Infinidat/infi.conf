from .test_utils import TestCase
from infi.conf import Config
from infi.conf import exceptions

class BasicUsageTest(TestCase):
    def setUp(self):
        super(BasicUsageTest, self).setUp()
        self.conf = Config(dict(
            a = dict(
                b = 2
                )
            ))
    def test__getting(self):
        self.assertEquals(self.conf.root.a.b, 2)
    def test__setting(self):
        self.conf.root.a.b = 3
        self.assertEquals(self.conf.root.a.b, 3)
    def test__setting_nonexistent_paths(self):
        with self.assertRaises(exceptions.CannotSetValue):
            self.conf['a']['c'] = 4
        with self.assertRaises(AttributeError):
            self.conf.root.a.c = 4
    def test__getting_through_getitem(self):
        self.assertIsInstance(self.conf['a'], Config)
    def test__setting_new_values(self):
        self.conf['c'] = Config(2)
        self.assertEquals(self.conf.root.c, 2)
        self.assertEquals(self.conf['c'], 2)
    def test__item_not_found(self):
        with self.assertRaises(LookupError):
            self.conf.root.a.c
    def test__keys(self):
        self.assertEquals(set(self.conf.keys()), set(['a']))


class LinkedConfigurationTest(TestCase):
    def setUp(self):
        super(LinkedConfigurationTest, self).setUp()
        self.conf1 = Config(dict(a=1))
        self.conf2 = Config(dict(c=2))
        self.conf1['b'] = self.conf2
    def test__linked_configurations(self):
        self.assertIs(self.conf1['b'], self.conf2)
    def test__linked_backup_and_restore(self):
        self.conf1.backup()
        self.conf2['c'] = 3
        self.assertEquals(self.conf1.root.b.c, 3)
        self.conf1['a'] = 2
        self.conf1.restore()
        self.assertEquals(self.conf1.root.b.c, 2)
    def test__linked_backups_restore_parent_then_child(self):
        self.conf2.backup()
        self.conf1.backup()
        self.conf2['c'] = 4
        self.assertEquals(self.conf2.root.c, 4)
        self.conf1.restore()
        self.assertEquals(self.conf2.root.c, 2)
        self.conf2['c'] = 5
        self.assertEquals(self.conf2.root.c, 5)
        self.conf2.restore()
        self.assertEquals(self.conf2.root.c, 2)

class BackupTest(TestCase):
    def setUp(self):
        super(BackupTest, self).setUp()
        self.conf = Config(dict(a=1, b=2))
    def test__restore_no_backup(self):
        with self.assertRaises(exceptions.NoBackup):
            self.conf.restore()
