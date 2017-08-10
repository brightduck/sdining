import xadmin

from .models import OAuthQQProfile, Accesstoken


class OAuthQQProfileAdmin:
    pass


class AccesstokenAdmin:
    list_display = (
        'access_token',
        'date_create',
    )

    readonly_fields = (
        'access_token',
    )


xadmin.site.register(OAuthQQProfile, OAuthQQProfileAdmin)
xadmin.site.register(Accesstoken, AccesstokenAdmin)
