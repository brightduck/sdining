import xadmin

from .models import OAuthQQProfile, Accesstoken


class OAuthQQProfileAdmin:
    pass


xadmin.site.register(OAuthQQProfile, OAuthQQProfileAdmin)
xadmin.site.register(Accesstoken)
