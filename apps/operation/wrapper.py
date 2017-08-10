from django.utils import timezone
from django.conf import settings

from .models import BusinessOrderList, Order

def push(order_list):
    # TODO PUSH
    pass

def wrapper_order_list(business_obj):

    minterval = settings.WRAPPER_MINUTE

    order_list = Order.objects.filter(is_accept=False, food__business=business_obj, is_push=False)

    if timezone.now().strftime("%H,%M") in settings.MUST_PUSH_ORDER_TIME:
        push(order_list=order_list)
    else:
        if order_list.count() < 10:
            pass
        else:
            push(order_list=order_list)
            for order in order_list:
                order.is_push = True
                order.save()

