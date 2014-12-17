#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup


def get_version():
    """Gets the repository version."""
    import subprocess
    proc = subprocess.Popen('hg log -r tip --template "{latesttagdistance}"',
                            shell=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pending, _ = proc.communicate()
    return "%(pending)s" % dict(pending=pending)


setup(name='weblib',
      version=get_version(),
      packages=['weblib'],
      install_requires=[req for req in open('requirements.txt').readlines()
                        if '-e' not in req])
