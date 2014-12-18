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
      install_requires=[
          'Jinja2==2.7.3',
          'SQLAlchemy==0.9.8',
          'celery==3.1.17',
          'oauth2==1.5.211',
          'redis==2.10.3',
          'web.py==0.37',
          'webassets==0.10.1',
      ])
