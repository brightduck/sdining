from django.conf import settings

from account.models import User
from account.qqapi import OAuthQQ


def changeavatar():
    oauth_qq = OAuthQQ(settings.APPID, settings.APPKEY, settings.REDIRECT_URI)
    for u in User.objects.filter(usertype=1):
        try:
            u.avatar = oauth_qq.get_user_qq_profile(openid=u.username)['headimgurl']
            u.save()
        except:
            pass
