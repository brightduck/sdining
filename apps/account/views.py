import time

from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.views.generic.base import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.shortcuts import render

from .qqapi import OAuthQQ
from .models import User, OAuthQQProfile
from .forms import BusinessApplyForm


def qq_login():
    oauth_qq = OAuthQQ(settings.APPID, settings.APPKEY, settings.REDIRECT_URI)
    url = oauth_qq.get_auth_url()
    return url


def try_openid(request, openid):
    qprofile = OAuthQQProfile.objects.filter(qq_openid=openid)
    if qprofile:
        u = qprofile[0].user
        if u.is_active:
            login(request, u)
            return 1
        else:
            login(request, u)
            return 2
    return 0


def qq_check(request):
    """
    for ucenter
    :param request: request object
    :return: to ucenter router
    """
    code = request.GET.get('code')
    oauth_qq = OAuthQQ(settings.APPID, settings.APPKEY, settings.REDIRECT_URI)
    try:
        openid, access_token = oauth_qq.get_open_id_and_token(code)
        status = try_openid(request, openid)
        if status == 1:
            return HttpResponseRedirect(reverse('ucenterindex'))
        elif status == 2:
            return HttpResponseRedirect(reverse('authguide'))
    except Exception:
        return HttpResponseRedirect(reverse('ucenterindex'))
    if not oauth_qq.get_user_status(openid) in [2, 4]:
        try:
            u = User.objects.create_user(username=openid, password=settings.DEFAULT_PASSWORD, usertype=0,
                                         is_active=False)
            OAuthQQProfile.objects.create(user=u, qq_openid=openid, access_token=access_token)
            login(request, u)
        except Exception:
            pass
        finally:
            return HttpResponseRedirect(reverse('authguide'))

    try:
        user_qq_profile = oauth_qq.get_user_qq_profile(openid)
        user_profile = oauth_qq.get_user_profile(openid)
    except Exception:
        return HttpResponseRedirect(reverse('ucenterindex'))
    try:
        u = User.objects.create_user(avatar=user_qq_profile['headimgurl'], username=user_qq_profile['openid'],
                                     password=access_token, truename=user_profile['name'])
        qprofile = OAuthQQProfile.objects.create(user=u, qq_openid=openid, access_token=access_token,
                                                 nickname=user_qq_profile['nickname'],
                                                 sex=user_qq_profile['sex'], stuid=user_profile['school_no'])
    except Exception:
        return HttpResponseForbidden()
    login(request, qprofile.user)
    return HttpResponseRedirect(reverse('ucenterindex'))


class LogoutView(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')


class AuthGuideView(LoginRequiredMixin, TemplateView):
    raise_exception = True
    template_name = 'auth/guide.html'


class AuthView(LoginRequiredMixin, TemplateView):
    raise_exception = True
    template_name = 'auth/auth.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        authapply_form = BusinessApplyForm()
        context['form'] = authapply_form
        return self.render_to_response(context)

    def post(self, request):
        if request.user.is_active:
            return HttpResponseForbidden()
        authapply_form = BusinessApplyForm(data=request.POST)
        if authapply_form.is_valid():
            try:
                newauthapply = authapply_form.save(commit=False)
                newauthapply.user = request.user
                newauthapply.save()
                newauthapply.user.phonenumber = authapply_form.cleaned_data['phonenumber']
                newauthapply.user.save()

                return render(request, 'auth/auth.html', {
                    'success': "您提交的申请正在审核中"
                })
            except:
                return render(request, 'auth/auth.html', {
                    'error': "请不要重复提交"
                })
        else:
            return render(request, 'auth/auth.html', {
                'form': authapply_form,
            })
