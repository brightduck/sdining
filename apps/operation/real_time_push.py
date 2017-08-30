from django.conf import settings

from account.qqapi import OAuthQQ


def push(openid, ordernum=1):
    oauth_qq = OAuthQQ(settings.APPID, settings.APPKEY, settings.REDIRECT_URI)
    data = {
        "tousername": openid,
        "templateid": settings.TEMPLATE_ID,
        "data": {
            "keynote1": {
                "value": str(ordernum)
            },
        },
        "button": {
            "button1": {
                "value": settings.TEMPLATE_BUTTON_URI
            }
        }
    }

    try:
        result = oauth_qq.send_message_from_template(postdata=data)
    except:
        pass