Overview
--------

infi.conf is a generic mechanism for storing, loading and manipulating configuration.

Usage
-----

Basics
======

Given a file like this::

 >>> f = open("/tmp/my_file.cfg", "wb")
 >>> f.write("""
 ... CONFIG = {
 ...    "a" : {
 ...       "b" : 2,
 ...    }
 ... }""")
 >>> f.close()

Obtaining a configuration object is done via::

 >>> from infi.conf import Config
 >>> c = Config.from_filename("/tmp/my_file.cfg")
 >>> c.root.a.b
 2

Loading From Other Sources
==========================

You can also load from string::

 >>> c = Config.from_string("CONFIG = {'a' : 2}")
 >>> c.root.a
 2

Updating Paths
==============

Setting paths is done by settings items::

 >>> c['a'] = 3
 >>> c.root.a
 3

Setting paths that didn't exist before is not allowed, unless you assign a config object::

 >>> c['b'] = 3 #doctest: +IGNORE_EXCEPTION_DETAIL
 Traceback (most recent call last):
  ...
 AttributeError: Cannot set attribute 'b'

 >>> c['b'] = Config(2)
 >>> c.root.b
 2

Backing Up/Restoring
====================

Whenever you want to preserve the configuration prior to a change and restore it later, you can do it with *backup()* and *restore()*. They work like a stack, so they push and pop states::

 >>> c = Config({"value":2})
 >>> c['value']
 2
 >>> c.backup()
 >>> c['value'] = 3
 >>> c['value']
 3
 >>> c.backup()
 >>> c['value'] = 4
 >>> c['value']
 4
 >>> c.restore()
 >>> c['value']
 3
 >>> c.restore()
 >>> c['value']
 2

