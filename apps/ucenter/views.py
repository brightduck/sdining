from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from operation.models import Order

NOTFOUNDMESSAGE = '跟你说了不要瞎点，你就是不听，好了捏，你一点看到一片白就以为是系统的错，一看到系统错就联系开发团队，一联系开发团队后端爸爸就要加班，后端一加班就烦，\
一烦就出错，你说你乱点个锤子'


class CustomerUcenterView(LoginRequiredMixin, TemplateView):
    login_url = '/admin/'
    template_name = 'ucenter/index.html'


@login_required(login_url='/admin/')
def order_is_done(request):
    oid = request.GET.get('id', '')
    if not oid:
        return HttpResponseNotFound(NOTFOUNDMESSAGE)
    try:
        obj = Order.objects.get(pk=int(oid), user=request.user)
        obj.is_done = True
        obj.save()
        return HttpResponseRedirect(reverse('ucenterindex'))
    except:
        return HttpResponseNotFound(NOTFOUNDMESSAGE)
