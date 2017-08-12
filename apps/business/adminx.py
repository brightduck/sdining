import xadmin
from xadmin.layout import Fieldset, Main, Side

from .models import Business, Food, Special, Authapply


class BusinessAdmin:
    list_display = (
        'name',
        'user',
        'type',
        'is_open'
    )

    search_fields = (
        'name',
    )

    list_filter = (
        'floor',
        'type',
        'position',
    )

    form_layout = (
        Main(
            Fieldset('基本信息',
                     'user',
                     'name',
                     'position',
                     'type',
                     'floor',
                     'image',
                     'average',
                     'num_like')
        ),
        Side(
            Fieldset('状态控制',
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
    list_filter = (
        'business',
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

class SpecialAdmin:
    pass

class AuthapplyAdmin:
    list_display = (
        'name',
        'position',
        'type',
        'is_passed',
        'date_apply'
    )

    list_filter = (
        'position',
        'type',
        'floor',
        'date_apply'
    )

    form_layout = (
        Main(
          Fieldset(
              '申请内容',
              'user',
              'name',
              'position',
              'floor',
              'type',
              'date_apply'
          ),
        ),
        Side(
            Fieldset(
                '状态控制',
                'is_passed',
            )
        )
    )

xadmin.site.register(Business, BusinessAdmin)
xadmin.site.register(Food, FoodAdmin)
xadmin.site.register(Special)
xadmin.site.register(Authapply, AuthapplyAdmin)
