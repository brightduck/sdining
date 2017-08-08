from django.shortcuts import render
from django.views.generic.base import TemplateView

from rest_framework import generics, permissions

from business.models import Business
from .serializers import BannerSerializer
from .models import Banner, Recommend

class IndexView(TemplateView):
    template_name = 'index/index.html'

    def get_context_data(self, **kwargs):
        kwargs = super(IndexView, self).get_context_data()
        kwargs['business_list'] = Business.objects.all()
        kwargs['recommend_list'] = Recommend.objects.all()
        return kwargs


    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.GET.get('position', '') == '1':
            context['business_list'] = context['business_list'].filter(position=1)
            context['recommend_list'] = context['recommend_list'].filter(business__position=1)
            return self.render_to_response(context)
        elif request.GET.get('position', '') == '2':
            context['business_list'] = context['business_list'].filter(position=2)
            context['recommend_list'] = context['recommend_list'].filter(business__position=2)
            return self.render_to_response(context)
        else:
            return self.render_to_response(context)






class APIBannerListView(generics.ListAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = (permissions.IsAuthenticated,)
