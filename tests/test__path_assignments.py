from .test_utils import TestCase
from infi.conf import Config
from infi.conf import utils
from infi.conf import exceptions

class PathAssignmentTest(TestCase):
    def setUp(self):
        super(PathAssignmentTest, self).setUp()
        self.conf = Config(dict(a=dict(b=dict(c=3)), d=4))
    def tearDown(self):
        super(PathAssignmentTest, self).tearDown()
    def test__invalid_path_assignment_to_key(self):
        with self.assertRaises(exceptions.CannotSetValue):
            utils.assign_path(self.conf, "a.b.d", 3)
    def test__invalid_path_assignment_to_path(self):
        with self.assertRaises(exceptions.InvalidPath):
            utils.assign_path(self.conf, "a.g.d", 3)
    def test__invalid_path_getting(self):
        with self.assertRaises(exceptions.InvalidPath):
            utils.get_path(self.conf, "a.g.d")
    def test__get_path_direct(self):
        self.assertEquals(4, utils.get_path(self.conf, "d"))
    def test__path_deducing_with_none(self):
        self.conf['a']['b']['c'] = None
        self.assertIsNone(self.conf.root.a.b.c)
        with self.assertRaises(exceptions.CannotDeduceType):
            utils.assign_path_expression(self.conf, 'a.b.c=2', deduce_type=True)
    def test__path_deducing_with_compound_types(self):
        for initial_value, value in [
                ([1, 2, 3], ["a", "b", 3]),
                ((1, 2), (3, 4, 5))
        ]:
            self.conf["a"]["b"] = initial_value
            utils.assign_path_expression(self.conf, "a.b={0!r}".format(value), deduce_type=True)
            self.assertEquals(self.conf["a"]["b"], value)
    def test__path_deducing_with_booleans(self):
        for false_literal in ('false', 'False', 'no', 'n', 'No', 'N'):
            self.conf['a']['b']['c'] = True
            utils.assign_path_expression(self.conf, 'a.b.c={0}'.format(false_literal), deduce_type=True)
            self.assertFalse(self.conf.root.a.b.c)
        for true_literal in ('true', 'True', 'yes', 'y', 'Yes', 'Y'):
            self.conf['a']['b']['c'] = False
            utils.assign_path_expression(self.conf, 'a.b.c={0}'.format(true_literal), deduce_type=True)
            self.assertTrue(self.conf.root.a.b.c)
        for invalid_literal in ('trueee', 0, 23, 2.3):
            with self.assertRaises(ValueError):
                utils.assign_path_expression(self.conf, 'a.b.c={0}'.format(invalid_literal), deduce_type=True)
    def test__assign_path_direct(self):
        utils.assign_path(self.conf, 'd', 5)
        self.assertEquals(self.conf['d'], 5)
