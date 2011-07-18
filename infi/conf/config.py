import copy
from sentinels import NOTHING
from . import exceptions

class Config(object):
    _backups = None
    def __init__(self, value=None):
        super(Config, self).__init__()
        self._value = value
        self.root = ConfigProxy(self)
    def __getitem__(self, item):
        returned = self._value[item]
        if isinstance(returned, dict):
            return Config(returned)
        return returned
    def get(self, key, default=None):
        return self._value.get(key, default)
    def __setitem__(self, item, value):
        if not self._can_set_item(item, value):
            raise exceptions.CannotSetValue("Cannot set key {0!r}".format(item))
        if isinstance(value, Config):
            value = value._value
        self._value[item] = value
    def _can_set_item(self, item, value):
        return item in self._value or isinstance(value, Config)
    def keys(self):
        return self._value.keys()
    @classmethod
    def from_filename(cls, filename, namespace=None):
        with open(filename, "rb") as f:
            return cls.from_file(f, filename)
    @classmethod
    def from_file(cls, f, filename="?", namespace=None):
        ns = dict(__file__ = filename)
        if namespace is not None:
            ns.update(namespace)
        return cls.from_string(f.read(), namespace=namespace)
    @classmethod
    def from_string(cls, s, namespace = None):
        if namespace is None:
            namespace = {}
        else:
            namespace = dict(namespace)
        exec s in namespace
        return cls(namespace['CONFIG'])
    def backup(self):
        if self._backups is None:
            self._backups = []
        self._backups.append(copy.deepcopy(self._value))
    def restore(self):
        self._value = self._backups.pop()

class ConfigProxy(object):
    def __init__(self, conf):
        super(ConfigProxy, self).__init__()
        self._conf = conf
    def __getattr__(self, attr):
        value = self._conf[attr]
        if isinstance(value, Config):
            value = value._value
        if isinstance(value, dict):
            return ConfigProxy(value)
        return value
