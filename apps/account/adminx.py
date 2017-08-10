import xadmin

from .models import OAuthQQProfile


class OAuthQQProfileAdmin:
    pass


xadmin.site.register(OAuthQQProfile, OAuthQQProfileAdmin)
