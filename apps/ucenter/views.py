from django.views.generic import TemplateView
from django.views.generic.base import View
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from account.views import qq_login
from operation.models import Order, AbnormalOrder

NOTFOUNDMESSAGE = '跟你说了不要瞎点，你就是不听，好了捏，你一点看到一片白就以为是系统的错，一看到系统错就联系开发团队，一联系开发团队后端爸爸就要加班，后端一加班就烦，\
一烦就出错，你说你乱点个锤子'


class CustomerUcenterView(TemplateView):
    template_name = 'ucenter/index.html'

    def get(self, request, *args, **kwargs):
        try:
            if not request.user.usertype:
                return HttpResponseRedirect(reverse('businessucenterindex'))
        except:
            pass
        context = self.get_context_data(**kwargs)
        auth_url = qq_login()
        context['auth_url'] = auth_url
        return self.render_to_response(context)


class BusinessUcenterView(LoginRequiredMixin, TemplateView):
    template_name = 'ucenter/business_index.html'
    raise_exception = True

    def get(self, request, *args, **kwargs):
        if self.request.user.usertype:
            return HttpResponseRedirect(reverse('ucenterindex'))
        if not self.request.user.is_active:
            return HttpResponseRedirect(reverse('authguide'))
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


@login_required(login_url='/ucenter/')
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


@login_required(login_url='/ucenter/')
def changeopen(request):
    if request.user.usertype:
        return HttpResponseForbidden()
    else:
        try:
            b = request.user.business
            b.is_open = not b.is_open
            b.save()
            return HttpResponseRedirect(reverse('businessucenterindex'))
        except:
            return HttpResponseNotFound(NOTFOUNDMESSAGE)


@login_required(login_url='/ucenter/')
def accept_or_deny(request):
    if request.user.usertype:
        return HttpResponseForbidden()
    else:
        op = request.GET.get('op')
        try:
            opk = int(request.GET.get('opk'))
            b = request.user.business
            o = Order.objects.get(pk=opk, food__business=b)
        except:
            return HttpResponseNotFound(NOTFOUNDMESSAGE)
        if op == 'accept':
            o.is_accept = True
            o.save()
        elif op == 'deny':
            o.delete()

        return HttpResponseRedirect(reverse('businessucenterindex'))


class ComplainView(LoginRequiredMixin, View):
    raise_exception = True

    def post(self, request):
        opk = request.POST.get('opk', False)
        try:
            o = Order.objects.get(pk=opk)
            o.is_abnormal = True
            o.save()
            AbnormalOrder.objects.create(order=o)
            o.user.creditrank = o.user.creditrank - 20
            o.user.can_order = False
            o.user.save()
            return JsonResponse({'status': 1})
        except:
            return JsonResponse({'status': 0})


class AboutmeView(TemplateView):
    template_name = 'utils/about.html'


class AgreeView(TemplateView):
    template_name = 'utils/agree.html'
