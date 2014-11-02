#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
from setuptools import find_packages
from setuptools import setup


requirements = os.path.join(os.path.dirname(__file__), 'requirements.txt')
INSTALL_REQUIRES = open(requirements).read().split()


params = dict(
    name='weblib',
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
)

setup(**params)
