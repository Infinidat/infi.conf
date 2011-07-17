import copy
from sentinels import NOTHING

class Config(object):
    _backups = None
    def __init__(self, value=None):
        super(Config, self).__init__()
        self._value = value
        self.root = ConfigProxy(self)
    def __getitem__(self, item):
        returned = self._value[item]
        return returned
    def __setitem__(self, item, value):
        if item not in self._value and not isinstance(value, Config):
            raise AttributeError("Cannot set attribute {!r}".format(item))
        self._value[item] = value
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
