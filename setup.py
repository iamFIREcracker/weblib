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
    return "%(tag)sd%(pending)s" % dict(tag='0.0.1', pending=pending)


PARAMS = dict(
)

setup(name='weblib',
      version=get_version(),
      packages=['weblib'],
      install_requires=[
          'Jinja2==2.7',
          'Mako==0.8.1',
          'MarkupSafe==0.18',
          'SQLAlchemy==0.8.1',
          'Werkzeug==0.8.3',
          'anyjson==0.3.3',
          'argparse==1.2.1',
          'celery==3.0.19',
          'distribute==0.6.24',
          'httplib2==0.8',
          'oauth2==1.5.211',
          'python-dateutil==2.1',
          'redis==2.7.5',
          'web.py==0.37',
          'webassets==0.8',
          'wsgiref==0.1.2',
      ])
