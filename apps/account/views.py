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


# def my_key(group, request):
#     return request.META['REMOTE_ADDR'] + request.POST['username']


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

# class LoginView(TemplateView):
#     template_name = 'auth/login.html'
#
#     def get(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return HttpResponseRedirect('/')
#         context = self.get_context_data(**kwargs)
#         return self.render_to_response(context)
#
#     @ratelimit(key=my_key, method='POST', rate='10/m')
#     def post(self, request):
#         login_form = LoginForm(request.POST)
#         was_limited = getattr(request, 'limited', False)
#         if was_limited:
#             return HttpResponseForbidden()
#         if login_form.is_valid():
#             username, password = login_form.cleaned_data['username'], login_form.cleaned_data['password']
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('businessucenterindex'))
#             else:
#                 return render(request, 'auth/login.html', {
#                     'mainerror': '请输入正确的授权号以及授权密码，如遗忘可联系开发团队'
#                 })
#         else:
#             return render(request, 'auth/login.html', {
#                 'form': login_form
#             })
