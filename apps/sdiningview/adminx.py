import xadmin
from xadmin import views

from .models import Banner, Recommend


# Base Settings
class BaseSetting:
    enable_themes = True


# global Settings
class GlobalSettings:
    site_title = '智慧食堂后台管理'
    site_footer = 'Powered By Tencent'



class BannerAdmin:
    pass


class RecommendAdmin:
    pass


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)

xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(Recommend, RecommendAdmin)
