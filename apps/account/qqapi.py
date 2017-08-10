import json
import urllib
from urllib import parse


class OAuthQQ(object):
    def __init__(self, appid, appkey, redirect_uri):
        self.appid = appid
        self.appkey = appkey
        self.redirect_uri = redirect_uri

    def get_auth_url(self):
        params = {
            'appid': self.appid,
            'response_type': 'code',
            'redirect_uri': self.redirect_uri,
            'state': 1
        }
        url = 'https://api.uni.qq.com/connect/oauth2/authorize?{}'.format(parse.urlencode(params))
        return url

    def get_open_id(self, code):
        params = {
            'grant_type': 'authorization_code',
            'appid': self.appid,
            'secret': self.appkey,
            'code': code,
        }
        url = 'https://api.uni.qq.com/sns/oauth2/access_token?{}'.format(parse.urlencode(params))
        return url
