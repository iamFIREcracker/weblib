#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
from setuptools import find_packages
from setuptools import setup


def get_version():
    """Gets the repository version."""
    import subprocess
    proc = subprocess.Popen(
            'hg log -r tip --template "{latesttagdistance}"',
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pending, _ = proc.communicate()
    return "%(tag)sd%(pending)s" % dict(tag='0.0.1', pending=pending)


params = dict(
    name='weblib',
    version=get_version(),
    packages=['weblib']
)

setup(**params)
