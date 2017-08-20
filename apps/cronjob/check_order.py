from django.utils import timezone

from operation.models import Order, AbnormalOrder


def check_order():
    now = timezone.now()
    for o in Order.objects.filter(is_accept=True, is_done=False, is_abnormal=False, is_push=True, is_comment=False):
        ocreate = o.date_create
        if (now - ocreate).total_seconds() >= 14400:
            o.is_abnormal = True
            o.save()
            a = AbnormalOrder(order=o)
            a.save()

    for o in Order.objects.filter(is_accept=False, is_done=False, is_abnormal=False, is_comment=False):
        o.is_abnormal = True
        o.save()
        a = AbnormalOrder(order=o)
        a.save()