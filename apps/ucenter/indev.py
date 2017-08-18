from django.views.generic import TemplateView


class MycollectView(TemplateView):
    '''
    我的收藏
    '''
    template_name = 'utils/underbuild.html'


class Myvouchers(TemplateView):
    '''
    我的礼券
    '''
    template_name = 'utils/underbuild.html'
