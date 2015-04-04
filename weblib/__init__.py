#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
from web.webapi import _status_code
from web.webapi import Redirect

from weblib.logging import create_logger


nocontent = NoContent = _status_code("204 No Content")


class Created(Redirect):
    """A `201 Created` response."""
    def __init__(self, url, absolute=False):
        Redirect.__init__(self, url, '201 Created', absolute=absolute)

created = Created


def internalerror(title):
    def inner():
        message = '''
%(title)s\n
method: %(method)s
fullpath: %(fullpath)s
env: %(env)s

''' % dict(title=title,
           method=web.ctx.method,
           fullpath=web.ctx.fullpath,
           env=web.ctx.environ
           )
        create_logger().exception(message)
        raise web.internalerror('Holy shit!')
    return inner
