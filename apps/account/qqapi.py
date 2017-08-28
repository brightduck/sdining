import json
import ssl
from urllib import parse, request

from django.utils import timezone

from .models import Accesstoken


class OAuthQQ(object):
    '''
    For QQ OAuth2.0 Auto Login
    '''
    context = ssl._create_unverified_context()

    def __init__(self, appid, appkey, redirect_uri):
        self.appid = appid
        self.appkey = appkey
        self.redirect_uri = redirect_uri

    def get_result(self, url, data=None):
        if data:
            response = request.urlopen(url, data, context=self.context)
        else:
            response = request.urlopen(url, context=self.context)
        result = json.load(response)
        return result

    def process_wrong_access_token(self, params, url, data=None):
        params['access_token'] = self.get_access_token(forced=True)
        url = url.format(parse.urlencode(params))
        if data:
            result = self.get_result(url, data)
        else:
            result = self.get_result(url)
        return result

    def get_access_token(self, forced=False):
        def get_accesstoken_from_qq():
            params = {
                'appid': self.appid,
                'secret': self.appkey
            }
            url = 'https://api.uni.qq.com/cgi-bin/token_v2?{}'.format(parse.urlencode(params))
            result = self.get_result(url)
            a = Accesstoken(access_token=result['access_token'], date_create=timezone.now())
            a.save()
            return a.access_token

        def delete_all_accesstoken():
            for a in Accesstoken.objects.all():
                a.delete()

        def check_accesstoken():
            try:
                a = Accesstoken.objects.all()[0]
            except:
                return False
            if (timezone.now() - a.date_create).total_seconds() < 7200:
                return a.access_token
            else:
                return False

        if forced:
            delete_all_accesstoken()
            return get_accesstoken_from_qq()
        else:
            if check_accesstoken():
                return check_accesstoken()
            else:
                return get_accesstoken_from_qq()

    def get_auth_url(self):
        params = {
            'appid': self.appid,
            'response_type': 'code',
            'redirect_uri': self.redirect_uri,
            'state': 1
        }
        url = 'https://api.uni.qq.com/connect/oauth2/authorize?{}'.format(parse.urlencode(params))
        return url

    def get_open_id_and_token(self, code):
        params = {
            'grant_type': 'authorization_code',
            'appid': self.appid,
            'secret': self.appkey,
            'code': code,
        }
        url = 'https://api.uni.qq.com/sns/oauth2/access_token?{}'.format(parse.urlencode(params))
        result = self.get_result(url)
        return (result['openid'], result['access_token'])

    def from_token_get_openid(self, access_token):
        params = {
            'access_token': access_token
        }
        url = 'https://api.uni.qq.com/sns/oauth2/openid?{}'.format(parse.urlencode(params))
        result = self.get_result(url)
        return result['openid']

    def get_user_status(self, openid):
        params = {
            'access_token': self.get_access_token(),
            'openid': openid
        }
        url = 'https://api.uni.qq.com/cgi-bin/certfans/status?{}'.format(parse.urlencode(params))
        result = self.get_result(url)
        try:
            if result['errcode'] == 40001:
                result = self.process_wrong_access_token(params=params,
                                                         url='https://api.uni.qq.com/cgi-bin/certfans/status?{}')
        except Exception as e:
            print(e)
            pass

        return result['status']

    def get_user_profile(self, openid):
        params = {
            'access_token': self.get_access_token(),
            'openid': openid
        }
        url = 'https://api.uni.qq.com/cgi-bin/certfans/info?{}'.format(parse.urlencode(params))
        result = self.get_result(url)
        try:
            if result['errcode'] == 40001:
                result = self.process_wrong_access_token(params=params,
                                                         url='https://api.uni.qq.com/cgi-bin/certfans/info?{}')
        except Exception as e:
            print(e)
            pass
        return result

    def get_user_qq_profile(self, openid):
        params = {
            'access_token': self.get_access_token(),
            'openid': openid,
            'lang': 'zh_CN'
        }
        url = 'https://api.uni.qq.com/cgi-bin/user/info?{}'.format(parse.urlencode(params))
        result = self.get_result(url)
        try:
            if result['errcode'] == 40001:
                result = self.process_wrong_access_token(params=params,
                                                         url='https://api.uni.qq.com/cgi-bin/user/info?{}')
        except Exception as e:
            print(e)
            pass
        return result

    def send_message_from_template(self, postdata):
        params = {
            'access_token': self.get_access_token(),
        }
        data = json.dumps(postdata)
        data = bytes(data, 'utf-8')

        url = 'https://api.uni.qq.com/cgi-bin/message/template/send?{}'.format(parse.urlencode(params))
        result = self.get_result(url, data=data)
        try:
            if result['errcode'] == 40001:
                result = self.process_wrong_access_token(params=params,
                                                         url='https://api.uni.qq.com/cgi-bin/message/template/send?{}',
                                                         data=data)
        except Exception as e:
            print(e)
            pass
        return result
