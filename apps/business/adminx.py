import xadmin
from xadmin.layout import Fieldset, Main, Side

from .models import Business, Food, Special, Authapply, BusinessTextComment


class BusinessAdmin:
    list_display = (
        'name',
        'user',
        'type',
        'is_open',
        'sort_weight'
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
                     'rank',
                     'total_rank',
                     'num_like',
                     'sort_weight')
        ),
        Side(
            Fieldset('状态控制',
                     'is_open'
                     ),
        ),
    )


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
                     'image', )
        ),
        Side(
            Fieldset('状态',
                     'can_reserve'
                     ),
        ),
    )


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


class BusinessTextCommentAdmin:
    list_display = (
        'comment',
        'business',
        'is_pass',
        'date_comment'
    )

    list_filter = (
        'is_pass',
        'date_comment',
    )

    search_fields = (
        'comment',
    )

    form_layout = (
        Main(
            Fieldset(
                '基本信息',
                'business',
                'comment',
                'date_comment'
            ),
        ),
        Side(
            Fieldset(
                '状态控制',
                'is_pass',
            )
        )
    )


xadmin.site.register(Business, BusinessAdmin)
xadmin.site.register(Food, FoodAdmin)
xadmin.site.register(Special)
xadmin.site.register(Authapply, AuthapplyAdmin)
xadmin.site.register(BusinessTextComment, BusinessTextCommentAdmin)
