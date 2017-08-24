from django.utils import timezone
from django.conf import settings

from account.qqapi import OAuthQQ

def push(openid):
    oauth_qq = OAuthQQ(settings.APPID, settings.APPKEY, settings.REDIRECT_URI)
    data = {
        "tousername": openid,
        "templateid": settings.TEMPLATE_ID,
        "data": {
            "keynote1": {
                "value": "1"
            },
        },
        "button": {
            "button1": {
                "value": settings.TEMPLATE_BUTTON_URI
            }
        }
    }

    oauth_qq.send_message_from_template(postdata=data)
    return True
