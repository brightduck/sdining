from django.utils import timezone

from account.models import User


def process_creditrank():
    for u in User.objects.filter(can_order=False):
        if (timezone.now() - u.date_ban).days == u.banday:
            u.can_order = True
            u.save()
        else:
            banday = (100 - u.creditrank) * 0.15
            u.banday = banday
            u.save()
