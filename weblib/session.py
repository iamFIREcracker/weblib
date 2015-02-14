#!/usr/bin/env python

import datetime

from web.session import Store


def _redis_key(key):
    return 'webpy.session' + key


def _datetime_to_int(dt):
    return int(float(dt.strftme('%s.%f') * 1000000))


class RedisStore(Store):
    """Store for saving a session in Redis.

    This store will create a key `webpy.sessions` containing all the
    active sessions, and a key for each of those sessions."""

    def __init__(self, redis):
        self._redis = redis

    def __contains__(self, key):
        return self._redis.get(_redis_key(key)) is not None

    def __getitem__(self, key):
        data = self.decode(self._redis.get(_redis_key(key)))
        value = data['value']
        now_int = data['now_int']
        self._redis.zrem('webpy.sessions', now_int)
        self[key] = value
        return value

    def __setitem__(self, key, value):
        redis_key = _redis_key(key)
        now_int = _datetime_to_int(datetime.datetime.now())
        data = self.encode(dict(value=value, now_int=now_int))
        self._redis.set(redis_key, data)
        self._redis.zadd('webpy.sessions', now_int, key)

    def __delitem__(self, key):
        self._redis.delete(_redis_key(key))

    def cleanup(self, timeout):
        seconds_to_days = 24.0 * 60 * 60
        timeout = datetime.timedelta(timeout / seconds_to_days)
        last_allowed_time = datetime.datetime.now() - timeout
        last_allowed_time_int = _datetime_to_int(last_allowed_time)
        for (key, now_int) in self._redis.zrange('webpy.sessions', 0,
                                                 last_allowed_time_int,
                                                 withscores=True):
            self._redis.zrem('webpy.sessions', now_int)
            del self[key]
