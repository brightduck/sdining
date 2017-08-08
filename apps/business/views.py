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
    permission_classes = (permissions.IsAuthenticated,)


class IsOwnerOrSuperuserOrReadOnly(permissions.BasePermission):
    '''
    For APIFoodDetailView
    A simple permission control for FoodAPI
    '''

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.business.user == request.user or request.user.is_superuser


class APIFoodDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrSuperuserOrReadOnly)
