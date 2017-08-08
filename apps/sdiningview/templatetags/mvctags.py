from django import template

from business.models import Business
register = template.Library()



@register.simple_tag
def business_type_filter(obj_list, type):
    if type == 1:
        return obj_list.filter(type=1)
    elif type == 2:
        return obj_list.filter(type=2)
    else:
        return obj_list