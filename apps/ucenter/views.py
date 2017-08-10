from django.views.generic import TemplateView
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from account.views import qq_login
from operation.models import Order

NOTFOUNDMESSAGE = '跟你说了不要瞎点，你就是不听，好了捏，你一点看到一片白就以为是系统的错，一看到系统错就联系开发团队，一联系开发团队后端爸爸就要加班，后端一加班就烦，\
一烦就出错，你说你乱点个锤子'


class CustomerUcenterView( TemplateView):
    login_url = '/admin/'
    template_name = 'ucenter/index.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        auth_url = qq_login()
        context['auth_url'] = auth_url
        return self.render_to_response(context)


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
