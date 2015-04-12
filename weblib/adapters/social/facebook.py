#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import hmac
import json
import urllib2

import requests
from weblib.pubsub import Publisher


class FacebookAdapter(object):
    """Defines a tiny adapter of the Facebook Graph API."""

    PROFILE = 'https://graph.facebook.com/me?access_token=%(token)s'

    def profile(self, access_token):
        url = self.PROFILE % dict(token=access_token)
        try:
            return (requests.get(url).json(), None)
        except urllib2.HTTPError as e:
            return (None, ('Unable to contact the server', url, str(e)))

    AVATAR = 'https://graph.facebook.com/%(id)s/picture?width=200&height=200'

    def name(self, first_name, last_name):
        if last_name:
            last_name = last_name[0] + '.'
        return ' '.join([first_name, last_name])

    def avatar_unresolved(self, user_id):
        return self.AVATAR % dict(id=user_id)

    def avatar(self, user_id):
        url = self.avatar_unresolved(user_id)
        r = requests.get(url, allow_redirects=False)
        return r.headers['Location']

    MUTUAL_FRIENDS = ('https://graph.facebook.com'
                      '/v2.3/%(id)s?'
                      'fields=context.fields(mutual_friends{first_name,last_name,picture}).limit(10)&'
                      'appsecret_proof=%(appsecret_proof)s&'
                      'access_token=%(token)s&')

    def mutual_friends(self, app_secret, access_token, other_user_id):
        appsecret_proof = hmac.new(app_secret,
                                   msg=access_token,
                                   digestmod=hashlib.sha256).hexdigest()
        url = self.MUTUAL_FRIENDS % dict(id=other_user_id,
                                         appsecret_proof=appsecret_proof,
                                         token=access_token)
        try:
            data = requests.get(url).json()
            if 'context' in data \
                    and 'mutual_friends' in data['context']:
                return (data, None)
            return (None, ('Invalid Facebook response', url, str(data)))
        except urllib2.HTTPError as e:
            return (None, ('Unable to contact the server', url, str(e)))


class FacebookProfileGetter(Publisher):
    def perform(self, adapter, access_token):
        """Gets the profile information of the user identified by the specified
        access token.

        If something goes wrong while trying to access the profile info, a
        'profile_not_found' message will be published with the error cause;
        on the other hand, a 'profile_found' message containing the profile
        information will be sent back to subscribers."""
        (data, error) = adapter.profile(access_token)
        if error is not None:
            self.publish('profile_not_found', error)
        else:
            data['name'] = adapter.name(data['first_name'], data['last_name'])
            data['avatar_unresolved'] = adapter.avatar_unresolved(data['id'])
            data['avatar'] = adapter.avatar(data['id'])
            data['email'] = (data['email'] if 'email' in data
                             else 'fuckyou@stupid.api')
            self.publish('profile_found', data)


class FacebookMutualFriendsGetter(Publisher):
    def perform(self, adapter, app_secret, access_token, other_user_id):
        (data, error) = adapter.mutual_friends(app_secret,
                                               access_token,
                                               other_user_id)
        if error is not None:
            self.publish('mutual_friends_not_found', error)
        else:
            mutual_friends = data['context']['mutual_friends']
            summary = \
                dict(total_count=mutual_friends['summary']['total_count'])
            data = [dict(name=adapter.name(d['first_name'],
                                           d['last_name']),
                         avatar=d['picture']['data']['url'])
                    for d in mutual_friends['data']]
            self.publish('mutual_friends_found',
                         dict(summary=summary, data=data))


def _facebook_mutualfriends_cacheid(user_id, other_user_id):
    return 'facebook_mutualfriends:%s_%s' % (user_id, other_user_id)


class CachedFacebookMutualFriendsGetter(Publisher):
    def perform(self, redis, user_id, other_user_id):
        cache_id = _facebook_mutualfriends_cacheid(user_id, other_user_id)
        raw = redis.get(cache_id)
        if raw is None:
            self.publish('cached_mutual_friends_not_found', cache_id)
        else:
            self.publish('cached_mutual_friends_found', json.loads(raw))


class CachedFacebookMutualFriendsSetter(Publisher):
    def perform(self, redis, user_id, other_user_id, mutual_friends,
                expire):
        cache_id = _facebook_mutualfriends_cacheid(user_id, other_user_id)
        redis.set(cache_id, json.dumps(mutual_friends), ex=expire)
        self.publish('cached_mutual_friends_set', cache_id)
