import xadmin
from xadmin.layout import Fieldset, Main, Side

from .models import Business, Food


class BusinessAdmin:
    list_display = (
        'name',
        'user',
        'is_open'
    )

    search_fields = (
        'name',
    )

    list_filter = (
        'floor',
        'position',
    )

    form_layout = (
        Main(
            Fieldset('基本信息',
                     'user',
                     'name',
                     'position',
                     'floor',
                     'image',
                     'average',
                     'num_like')
        ),
        Side(
            Fieldset('状态',
                     'is_open'
                     ),
        ),
    )

    def queryset(self):
        qs = super(BusinessAdmin, self).queryset()
        if not self.user.is_superuser:
            qs = qs.filter(user=self.user)
        return qs

class FoodAdmin:
    list_display = (
        'business',
        'name',
        'can_reserve',
    )

    form_layout = (
        Main(
            Fieldset('基本信息',
                     'business',
                     'name',
                     'price',
                     'image',)
        ),
        Side(
            Fieldset('状态',
                     'can_reserve'
                     ),
        ),
    )

    def queryset(self):
        qs = super(FoodAdmin, self).queryset()
        if not self.user.is_superuser:
            pass
        return qs

xadmin.site.register(Business, BusinessAdmin)
xadmin.site.register(Food, FoodAdmin)
