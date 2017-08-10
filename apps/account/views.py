import time
import ssl

import requests

from django.http import HttpResponseRedirect
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth import login
from .qqapi import OAuthQQ
from .models import User, OAuthQQProfile

context = ssl._create_unverified_context()

def qq_login(request):
    oauth_qq = OAuthQQ(settings.APPID, settings.APPKEY, settings.REDIRECT_URI)
    url = oauth_qq.get_auth_url()
    return url

def qq_check(request):
    code = request.GET.get('code')
    oauth_qq = OAuthQQ(settings.APPID, settings.APPKEY, settings.REDIRECT_URI)

    openid, access_token = oauth_qq.get_open_id_and_token(code)
    time.sleep(0.1)
    qprofile = OAuthQQProfile.objects.filter(qq_openid=openid)

    if qprofile:
        login(request, qprofile[0].user)
        return HttpResponseRedirect('/')
    else:
        user_qq_profile = oauth_qq.get_user_qq_profile(openid)
        user_profile = oauth_qq.get_user_profile(openid)
        u = User.objects.create(avatar=user_qq_profile['headimgurl'], username=user_qq_profile['openid'])
        qprofile = OAuthQQProfile.objects.create(user=u, qq_openid=openid, access_token=access_token, nickname=user_qq_profile['nickname'],
                                  sex=user_qq_profile['sex'], stuid=user_profile['school_no'])
        login(request, qprofile.user)
        return HttpResponseRedirect('/')


