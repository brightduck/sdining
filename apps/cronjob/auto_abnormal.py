from operation.models import Order, AbnormalOrder

def auto_abnormal():
    order_list = Order.objects.filter(is_accept=False, is_abnormal=False)
    for o in order_list:
        o.is_abnormal = True
        AbnormalOrder.objects.create(order=o)
        o.save()