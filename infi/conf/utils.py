from sentinels import NOTHING
from .exceptions import InvalidPath
from .exceptions import CannotDeduceType

def assign_path(conf, path, value):
    if '.' in path:
        path, key = path.rsplit(".", 1)
        conf = get_path(conf, path)
    else:
        key = path
    conf[key] = value

def assign_path_expression(conf, expr, deduce_type=False):
    path, value = expr.split("=", 1)
    if deduce_type:
        leaf = get_path(conf, path)
        value = _coerce_leaf_value(path, value, leaf)
    assign_path(conf, path, value)

_VALUES_FOR_TRUE = ['yes', 'y', 'true', 't']
_VALUES_FOR_FALSE = ['no', 'n', 'false', 'f']

def _coerce_leaf_value(path, value, leaf):
    if leaf is None:
        raise CannotDeduceType("Cannot deduce type of path {0!r}".format(path))
    leaf_type = type(leaf)
    if leaf_type is bool:
        value = value.lower()
        if value not in _VALUES_FOR_TRUE and value not in _VALUES_FOR_FALSE:
            raise ValueError('Invalid value for boolean: {!r}'.format(value))
        return value in _VALUES_FOR_TRUE
    return leaf_type(value)

def get_path(conf, path):
    returned = conf
    path_components = path.split(".")
    for p in path_components:
        key = returned.get(p, NOTHING)
        if key is NOTHING:
            raise InvalidPath("Invalid path: {0!r}".format(path))
        returned = returned[p]
    return returned

def get_config_object_from_proxy(proxy):
    return proxy._conf
