from operation.models import Order

def auto_done():
    order_list = Order.objects.filter(is_accept=True, is_done=False, is_abnormal=False)
    for o in order_list:
        o.is_done = True
        o.save()