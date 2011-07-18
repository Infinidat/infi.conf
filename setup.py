
import os
import itertools
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), "infi","conf", "__version__.py")) as version_file:
    exec version_file.read()

setup(name="infi.conf",
      classifiers = [
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: BSD License",
          "Programming Language :: Python :: 2.7",
          ],
      description="Generic configuration mechanism",
      license="BSD",
      author="Rotem Yaari",
      author_email="vmalloc@gmail.com",
      url="https://github.com/vmalloc/infi.conf",
      version=__version__,
      packages=find_packages(exclude=["tests"]),
      install_requires=[],
      scripts=[],
      namespace_packages=["infi",]
      )
