from django import template

from operation.models import Order

register = template.Library()

from sdiningview.models import Banner


@register.simple_tag
def business_type_filter(obj_list, type):
    if type == 1:
        return obj_list.filter(type=1)
    elif type == 2:
        return obj_list.filter(type=2)
    else:
        return obj_list



@register.simple_tag
def get_banner():
    return Banner.objects.all()


@register.simple_tag
def get_pending_order_list(business_obj):
    return Order.objects.filter(food__business=business_obj, is_accept=False)

@register.simple_tag
def get_done_order_list(business_obj):
    return Order.objects.filter(food__business=business_obj, is_done=True)[:5]

@register.filter
def crenumlist(value):
    try:
        return range(value)
    except (TypeError, ValueError):
        return [0]