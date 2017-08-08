from django import template

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


@register.filter
def crenumlist(value):
    try:
        return range(value)
    except (TypeError, ValueError):
        return [0]