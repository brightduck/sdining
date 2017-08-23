from business.models import Business

def auto_close():
    for b in Business.objects.all():
        b.is_open = False
        b.save()
