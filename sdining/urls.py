from django.conf.urls import url, include
from django.views.static import serve
from django.conf import settings

from rest_framework.urlpatterns import format_suffix_patterns

import xadmin

from sdiningview import views as mainviews
from business import views as businessviews
from account import views as accountviews

urlpatterns = [
    url(r'^$', mainviews.IndexView.as_view(), name='index'),

    url(r'^mvcapi/$', mainviews.api_root, name='api_list'),
    url(r'^mvcapi/banner/$', mainviews.APIBannerListView.as_view(), name='banner_list_api'),
    url(r'^mvcapi/food/$', businessviews.APIFoodListView.as_view(), name='food_list_api'),
    url(r'^mvcapi/food/(?P<pk>[0-9]+)/$', businessviews.APIFoodDetailView.as_view(), name='food_detail_api'),
    url(r'^mvcapi/business/$', businessviews.APIBusinessListView.as_view(), name='business_list_api'),
    url(r'^mvcapi/business/(?P<pk>[0-9]+)/$', businessviews.APIBusinessDetailView.as_view(),
        name='business_detail_api'),

    url(r'admin/', include(xadmin.site.urls)),

    url(r'^media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),

    url(r'^mvcapi/', include('rest_framework.urls',
                               namespace='rest_framework')),

    url(r'^oauth/qq/check/$', accountviews.qq_login, name='qq_check'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
