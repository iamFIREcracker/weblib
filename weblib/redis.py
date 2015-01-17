#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import redis
import web

__all__ = ['create_redis']


def create_redis(address=None, port=None):
    if address is None:
        address = web.config.get('REDIS_ADDRESS', '127.0.0.1')
    if port is None:
        port = web.config.get('REDIS_PORT', 6379)
    return redis.Redis(host=address, port=port)


def create_redis_pool(address=None, port=None):
    if address is None:
        address = web.config.get('REDIS_ADDRESS', '127.0.0.1')
    if port is None:
        port = web.config.get('REDIS_PORT', 6379)
    pool = redis.ConnectionPool(host=address, port=port, db=0)
    def factory():
        return redis.Redis(connection_pool=pool)
    return factory
