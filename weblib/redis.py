#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import redis
import web

__all__ = ['create_redis']


def create_redis(host=None, port=None):
    if host is None:
        host = web.config.get('REDIS_HOST', 'localhost')
    if port is None:
        port = web.config.get('REDIS_PORT', 6379)
    return redis.Redis(host=host, port=port)
