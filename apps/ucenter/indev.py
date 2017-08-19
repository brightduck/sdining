from django.views.generic import TemplateView


class Myvouchers(TemplateView):
    '''
    我的礼券
    '''
    template_name = 'utils/underbuild.html'
