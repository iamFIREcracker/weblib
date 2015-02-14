#!/usr/bin/env python

import datetime

from web.session import Store


class RedisStore(Store):
    """Store for saving a session in Redis.

    This store will create a key `webpy.sessions` containing all the
    active sessions, and a key for each of those sessions."""

    def __init__(self, redis):
        self._redis = redis

    def _redis_key(self, key):
        return 'webpy.session:' + key

    def _datetime_to_float(self, dt):
        return int(float(dt.strftime('%s.%f')) * 1000000)

    def __contains__(self, key):
        return self._redis.get(self._redis_key(key)) is not None

    def __getitem__(self, key):
        data = self.decode(self._redis.get(self._redis_key(key)))
        value = data['value']
        now = data['now']
        self._redis.zrem('webpy.sessions', now)
        self[key] = value
        return value

    def __setitem__(self, key, value):
        redis_key = self._redis_key(key)
        now = self._datetime_to_float(datetime.datetime.now())
        data = self.encode(dict(value=value, now=now))
        self._redis.set(redis_key, data)
        self._redis.zadd('webpy.sessions', key, now)

    def __delitem__(self, key):
        self._redis.delete(self._redis_key(key))
        self._redis.zrem('webpy.sessions', key)

    def cleanup(self, timeout):
        last_allowed_time = \
            datetime.datetime.now() - datetime.timedelta(seconds=timeout)
        last_allowed_time = self._datetime_to_float(last_allowed_time)
        for (key, now) in self._redis.zrangebyscore('webpy.sessions',
                                                    0,
                                                    last_allowed_time,
                                                    score_cast_func=int,
                                                    withscores=True):
            del self[key]
