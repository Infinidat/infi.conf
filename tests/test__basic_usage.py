import unittest
from infi.conf import Config

class BasicUsageTest(unittest.TestCase):
    def setUp(self):
        super(BasicUsageTest, self).setUp()
        self.conf = Config(dict(
            a = dict(
                b = 2
                )
            ))
    def test__getting(self):
        self.assertEquals(self.conf.root.a.b, 2)
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
        self.assertItemsEqual(self.conf.keys(), ['a'])
