from django.shortcuts import render
from django.views.generic.base import TemplateView

from rest_framework import generics, permissions

from business.models import Food
from .serializers import BannerSerializer
from .models import Banner

class IndexView(TemplateView):
    template_name = 'index/index.html'

    def get_context_data(self, **kwargs):
        return Food.objects.all()

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.GET.get('position', '') == '1':
            context['food_list'] = context['food_list'].filter(business__position=1)
            return self.render_to_response(context)
        elif request.GET.get('position', '') == '2':
            context['food_list'] = context['food_list'].filter(business__position=2)
            return self.render_to_response(context)
        else:
            return self.render_to_response(context)






class APIBannerListView(generics.ListAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = (permissions.IsAuthenticated,)
