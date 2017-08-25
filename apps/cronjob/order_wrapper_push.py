from django.conf import settings

from operation.models import Order
from account.qqapi import OAuthQQ
from business.models import Business


def push(openid, ordernum):
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

    result = oauth_qq.send_message_from_template(postdata=data)
    if result['errcode'] == 0:
        return True
    else:
        return False


def wrapper():
    sortorder = {}

    for b in Business.objects.filter():
        sortorder[b] = []

    print(sortorder)
    for o in Order.objects.filter(is_accept=False, is_push=False):
        if o.food.business in sortorder:
            ob = o.food.business
            sortorder[ob].append(o)

    print(sortorder)

    for i in sortorder:
        count = len(sortorder[i])
        if count:
            if push(i.user.oauthqqprofile.qq_openid, count):
                for o in sortorder[i]:
                    o.is_push = True
                    o.save()
            else:
                pass
        else:
            pass
