from django.conf.urls import url, include
from django.views.static import serve
from django.conf import settings

from rest_framework.urlpatterns import format_suffix_patterns

import xadmin

from sdiningview import views as mainviews
from business import views as businessviews

urlpatterns = [
    url(r'^$', mainviews.IndexView.as_view(), name='index'),


    url(r'^mvcapi/banner_list/$', mainviews.APIBannerListView.as_view(), name='banner_list_api'),
    url(r'^mvcapi/food_list/$', businessviews.APIFoodListView.as_view(), name='food_list_api'),

    url(r'admin/', include(xadmin.site.urls)),

    url(r'^media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),
]

urlpatterns = format_suffix_patterns(urlpatterns)
