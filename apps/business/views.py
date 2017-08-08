from django.shortcuts import render
from django.views.generic.list import ListView

from rest_framework import generics, permissions

from .serializers import FoodSerializer
from .models import Food

class FoodList(ListView):
    CATWGORY_LIST = [
        'meals',
        'recommend',
        'drink',
    ]
    template_name = 'index/index.html'




class APIFoodListView(generics.ListAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = (permissions.IsAuthenticated, )
