from django.db import models
from django.contrib.auth.models import AbstractUser

from .validators import PhonenumberValidator
from storage.storage import ImgStorage


class User(AbstractUser):
    qq = models.CharField(max_length=15, unique=True, verbose_name="QQ号")
    phonenumber = models.CharField(max_length=11, validators=[PhonenumberValidator()], verbose_name="手机号")
    avatar = models.ImageField(upload_to='avatar/%Y/%m/%d', default='avatar/base_avatar.png', storage=ImgStorage(),
                               verbose_name="头像")
    creditrank = models.IntegerField(default=100, verbose_name="信用级别")

    def get_now_order_list(self):
        '''
        Retrive the orders which is accepted
        :return: order list
        '''
        return self.myorder.all().filter(is_accept=True, is_done=False)

    def get_done_order_list(self):
        return self.myorder.all().filter(is_accept=True, is_done=True)

    def save(self, *args, **kwargs):
        if not self.email:
            self.email = '{}@qq.com'.format(self.username)
        super(User, self).save()


class OAuthQQProfile(models.Model):
    user = models.OneToOneField(User, verbose_name="用户")
    qq_openid = models.CharField(max_length=64, blank=True)
    nickname = models.CharField(max_length=256, blank=True, verbose_name="昵称")
    sex = models.IntegerField(choices=((1, "男"), (2, "女"), (3, "未知")), verbose_name="性别", default=1)
    stuid = models.CharField(max_length=20, verbose_name="学号", blank=True)

    def __str__(self):
        return 'QQ: {} nickname: {}'.format(self.user.qq, self.nickname)

    class Meta:
        verbose_name = "QQ个人信息"
        verbose_name_plural = verbose_name
