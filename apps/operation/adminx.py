import xadmin
from xadmin.layout import Fieldset, Main, Side

from .models import Order, AbnormalOrder, BusinessOrderList


class OrderAdmin:
    list_display = (
        'user',
        'is_accept',
        'date_create',
        'is_done',
        'date_done',
    )

    list_filter = (
        'is_accept',
        'is_done',
        'is_abnormal',
        'comment',
    )

    search_fields = (
        'food',
        'user',
    )

    form_layout = (
        Main(
            Fieldset(
                "基本信息",
                'user',
                'food',
                'comment'
            ),
            Fieldset(
                "时间",
                'date_create',
                'date_done',
            ),
        ),
        Side(
            Fieldset(
                "状态控制",
                'is_accept',
                'is_done',
                'is_abnormal',
                'is_push',
            )
        )
    )

    def queryset(self):
        qs = super(OrderAdmin, self).queryset()
        if not self.user.is_superuser:
            qs = qs.filter(food__business__user=self.user)
        return qs

class AbnormalOrderAdmin:
    pass


class BusinessOrderListAdmin:
    pass

xadmin.site.register(Order, OrderAdmin)
xadmin.site.register(AbnormalOrder, AbnormalOrderAdmin)
xadmin.site.register(BusinessOrderList, BusinessOrderListAdmin)