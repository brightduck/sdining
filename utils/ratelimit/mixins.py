from __future__ import absolute_import

from ratelimit import ALL, UNSAFE
from ratelimit.decorators import ratelimit


__all__ = ['RatelimitMixin']


class RatelimitMixin(object):

    ratelimit_group = None
    ratelimit_key = None
    ratelimit_rate = '5/m'
    ratelimit_block = False
    ratelimit_method = ALL

    ALL = ALL
    UNSAFE = UNSAFE

    def get_ratelimit_config(self):
        # Ensures that the ratelimit_key is called as a function instead
        # of a method if it is a callable (ie self is not passed).
        if callable(self.ratelimit_key):
            self.ratelimit_key = self.ratelimit_key.__func__
        return dict(
            group=self.ratelimit_group,
            key=self.ratelimit_key,
            rate=self.ratelimit_rate,
            block=self.ratelimit_block,
            method=self.ratelimit_method,
        )

    def dispatch(self, *args, **kwargs):
        return ratelimit(
            **self.get_ratelimit_config()
        )(super(RatelimitMixin, self).dispatch)(*args, **kwargs)
