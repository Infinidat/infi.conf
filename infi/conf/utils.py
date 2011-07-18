from types import NoneType
from sentinels import NOTHING
from .exceptions import InvalidPath
from .exceptions import CannotDeduceType

def assign_path(conf, path, value):
    path, key = path.rsplit(".", 1)
    conf = get_path(conf, path)
    conf[key] = value

def assign_path_expression(conf, expr, deduce_type=False):
    path, value = expr.split("=", 1)
    if deduce_type:
        leaf_type = type(get_path(conf, path))
        if leaf_type is NoneType:
            raise CannotDeduceType("Cannot deduce type of path {0!r}".format(path))
    else:
        leaf_type = str
    assign_path(conf, path, leaf_type(value))

def get_path(conf, path):
    returned = conf
    path_components = path.split(".")
    for p in path_components:
        key = returned.get(p, NOTHING)
        if key is NOTHING:
            raise InvalidPath("Invalid path: {0!r}".format(path))
        returned = returned[p]
    return returned
