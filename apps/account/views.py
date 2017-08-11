import time
import ssl

from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import login, logout
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse

from .qqapi import OAuthQQ
from .models import User, OAuthQQProfile

context = ssl._create_unverified_context()


def qq_login():
    oauth_qq = OAuthQQ(settings.APPID, settings.APPKEY, settings.REDIRECT_URI)
    url = oauth_qq.get_auth_url()
    return url


def qq_check(request):
    '''
    for ucenter
    :param request: request object
    :return: to ucenter router
    '''
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('ucenterindex'))
    code = request.GET.get('code')
    oauth_qq = OAuthQQ(settings.APPID, settings.APPKEY, settings.REDIRECT_URI)
    try:
        openid, access_token = oauth_qq.get_open_id_and_token(code)
        print(openid, access_token)
    except:
        return HttpResponseRedirect(reverse('ucenterindex'))
    time.sleep(0.05)
    qprofile = OAuthQQProfile.objects.filter(qq_openid=openid)

    if qprofile:
        login(request, qprofile[0].user)
        return HttpResponseRedirect(reverse('ucenterindex'))
    else:
        try:
            user_qq_profile = oauth_qq.get_user_qq_profile(openid)
            user_profile = oauth_qq.get_user_profile(openid)
        except:
            return HttpResponseRedirect(reverse('ucenterindex'))
        try:
            u = User.objects.create_user(avatar=user_qq_profile['headimgurl'], username=user_qq_profile['openid'], password=access_token)
            qprofile = OAuthQQProfile.objects.create(user=u, qq_openid=openid, access_token=access_token,
                                                 nickname=user_qq_profile['nickname'],
                                                 sex=user_qq_profile['sex'], stuid=user_profile['school_no'])
        except:
            return HttpResponseRedirect('/admin/')
        login(request, qprofile.user)
        return HttpResponseRedirect(reverse('ucenterindex'))


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')
