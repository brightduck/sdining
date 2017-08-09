from django.db import models
from django.contrib.auth.models import AbstractUser

from .validators import PhonenumberValidator

class User(AbstractUser):
    qq = models.CharField(max_length=15, unique=True, verbose_name="QQ号")
    phonenumber = models.CharField(max_length=11, validators=[PhonenumberValidator()], verbose_name="手机号")
    creditrank = models.IntegerField(default=100, verbose_name="信用级别")


    def save(self, *args, **kwargs):
        if not self.email:
            self.email = '{}@qq.com'.format(self.username)
        super(User, self).save()




