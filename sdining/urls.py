from django.conf.urls import url, include
from django.views.static import serve
from django.conf import settings
from django.views.decorators.cache import cache_page

from rest_framework.urlpatterns import format_suffix_patterns
import xadmin

from sdiningview import views as mainviews
from business import views as businessviews
from ucenter import views as ucenterviews
from ucenter import indev as indeviews
from account import views as accountviews
from operation import views as operationviews

urlpatterns = [
    url(r'^$', mainviews.IndexView.as_view(), name='index'),

    url(r'^business/(?P<pk>[0-9]+)/$', businessviews.BusinessDetailView.as_view(), name='businessdetail'),

    url(r'^operation/makeorder/$', operationviews.makeorder, name='makeorder'),
    url(r'^operation/removeorder/$', operationviews.removeorder, name='removeorder'),
    url(r'^operation/showorder/$', operationviews.ShowOrderView.as_view(), name='showorder'),

    url(r'^ucenter/$', ucenterviews.CustomerUcenterView.as_view(), name='ucenterindex'),
    url(r'^ucenter/about/$', ucenterviews.AboutmeView.as_view(), name='about'),
    url(r'^ucenter/agree/$', ucenterviews.AgreeView.as_view(), name='agree'),
    url(r'^ucenter/done/$', ucenterviews.order_is_done, name='orderdone'),
    url(r'^ucenter/collect/$', operationviews.MycollectView.as_view(), name='mycollect'),
    url(r'^ucenter/business/$', ucenterviews.BusinessUcenterView.as_view(), name='businessucenterindex'),
    url(r'^ucenter/comment/(?P<opk>[0-9]+)/$', operationviews.comment, name='comment'),
    url(r'^ucenter/business/change/$', ucenterviews.changeopen, name='changestatus'),
    url(r'^ucenter/business/aord/$', ucenterviews.accept_or_deny, name='accept_or_deny'),

    url(r'^mvcapi/$', mainviews.api_root, name='api_list'),
    url(r'^mvcapi/banner/$', mainviews.APIBannerListView.as_view(), name='banner_list_api'),
    url(r'^mvcapi/food/$', businessviews.APIFoodListView.as_view(), name='food_list_api'),
    url(r'^mvcapi/food/(?P<pk>[0-9]+)/$', businessviews.APIFoodDetailView.as_view(), name='food_detail_api'),
    url(r'^mvcapi/business/$', businessviews.APIBusinessListView.as_view(), name='business_list_api'),
    url(r'^mvcapi/business/(?P<pk>[0-9]+)/$', businessviews.APIBusinessDetailView.as_view(),
        name='business_detail_api'),
    url(r'^mvcapi/', include('rest_framework.urls',
                             namespace='rest_framework')),

    url(r'^admin/', include(xadmin.site.urls)),

    url(r'^media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),

    url(r'^qq/login/$', accountviews.qq_login, name='qqlogin'),
    url(r'^qq/check/$', accountviews.qq_check, name='qqcheck'),

    url(r'^account/authguide/$', accountviews.AuthGuideView.as_view(), name='authguide'),
    url(r'^account/auth/$', accountviews.AuthView.as_view(), name='auth'),
    url(r'^account/logout/$', accountviews.LogoutView.as_view(), name='logout'),

    url(r'^indev/vouchers/$', indeviews.Myvouchers.as_view(), name='myvouchers'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
