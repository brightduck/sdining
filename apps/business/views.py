from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse

from rest_framework import generics, permissions
from rest_framework.response import Response

from .serializers import FoodSerializer, BusinessSerializer
from .models import Food, Business


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


class FoodIsOwnerOrSuperuserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.business.user == request.user or request.user.is_superuser


class APIFoodDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = (permissions.IsAuthenticated, FoodIsOwnerOrSuperuserOrReadOnly)


class APIBusinessListView(generics.ListAPIView):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        try:
            queryset = queryset.filter(position=int(request.GET['position']))
        except:
            pass
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BusinessIsOwnerOrSuperuserOrReadOnly(permissions.BasePermission):
    '''
    For APIBusinessDetailView
    A simple permission control for BusinessAPI
    '''

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user or request.user.is_superuser


class APIBusinessDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = (permissions.IsAuthenticated, BusinessIsOwnerOrSuperuserOrReadOnly)


class BusinessDetailView(LoginRequiredMixin, DetailView):
    model = Business
    template_name = 'business/detail.html'
    context_object_name = 'business'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        try:
            del request.session['order']
        except:
            pass
        return self.render_to_response(context)
