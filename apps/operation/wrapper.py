import json
import ssl
from urllib import request, parse

from django.utils import timezone
from django.conf import settings

from .models import BusinessOrderList, Order
from account.qqapi import OAuthQQ


def push(openid):
    # TODO PUSH
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
    postdata = json.dumps(data)
    postdata = bytes(postdata, 'utf-8')

    oauth_qq.send_message_from_template(postdata=postdata)
    return True


def wrapper_order_list(order_obj):
    minterval = settings.WRAPPER_MINUTE

    # order_list = Order.objects.filter(is_accept=False, food__business=business_obj, is_push=False)

    def check_time(nowstrftime):
        return True
        # for timestr in settings.ORDER_TIME_ONE:
        #     if nowstrftime > timestr[0] and nowstrftime < timestr[1]:
        #         return True
        #
        # for timestr in settings.ORDER_TIME_TWO:
        #     if nowstrftime > timestr[0] and nowstrftime < timestr[1]:
        #         return True
        #
        # return False

    if check_time(timezone.now().strftime("%H,%M")):
        if not minterval:
            if push(openid=order_obj.get_openid()):
                order_obj.is_push = True
                order_obj.save()
        else:
            pass
    else:
        pass
