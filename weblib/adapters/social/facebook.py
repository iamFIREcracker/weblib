#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import urllib2

import requests


class FacebookAdapter(object):
    """Defines a tiny adapter of the Facebook Graph API."""

    PROFILE = 'https://graph.facebook.com/me?access_token=%(token)s'

    def profile(self, access_token):
        url = self.PROFILE % dict(token=access_token)
        try:
            return (json.load(urllib2.urlopen(url)), None)
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
                      '&fields=context.fields(mutual_friends{first_name,last_name,picture}).limit(10)'
                      '&access_token=%(token)s')

    def mutual_friends(self, access_token, other_user_id):
        url = self.MUTUAL_FRIENDS % dict(id=other_user_id,
                                         token=access_token)
        try:
            return (json.load(urllib2.urlopen(url)), None)
        except urllib2.HTTPError as e:
            return (None, ('Unable to contact the server', url, str(e)))
