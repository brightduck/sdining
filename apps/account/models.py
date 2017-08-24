from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    avatar = models.URLField(blank=True, verbose_name="头像")
    creditrank = models.IntegerField(default=100, verbose_name="信用级别")
    usertype = models.IntegerField(choices=((0, "商家"), (1, "用户")), verbose_name="用户类型", default=1)
    phonenumber = models.CharField(max_length=11, blank=True, verbose_name="联系方式")
    truename = models.CharField(max_length=30, blank=True, verbose_name="真实姓名")

    can_order = models.BooleanField(verbose_name="是否能订餐", default=True)
    date_ban = models.DateTimeField(verbose_name="开始封禁的时间", blank=True, null=True)
    banday = models.IntegerField(default=0, verbose_name="封禁天数")

    def get_now_order_list(self):
        try:
            return self.myorder.all().filter(is_accept=True, is_done=False, is_abnormal=False)
        except:
            return None

    def get_done_order_list(self):
        try:
            return self.myorder.all().filter(is_accept=True, is_done=True, is_abnormal=False)[:5]
        except:
            return None

    def get_collect_list(self):
        try:
            return self.mycollect.business.all()
        except:
            return None

    def get_businessuser_now_order(self):
        try:
            return self.business.order_list.orders.all().order_by('-date_create').filter(is_abnormal=False)
        except:
            return None

    def save(self, *args, **kwargs):
        if self.can_order == True:
            self.banday = 0
        else:
            self.date_ban = timezone.now()
        super(User, self).save()


class Accesstoken(models.Model):
    access_token = models.CharField(max_length=200)
    date_create = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_create']


class OAuthQQProfile(models.Model):
    user = models.OneToOneField(User, verbose_name="用户")
    qq_openid = models.CharField(max_length=100, blank=True)
    access_token = models.CharField(max_length=100, blank=True)
    nickname = models.CharField(max_length=256, blank=True, verbose_name="昵称")
    sex = models.IntegerField(choices=((1, "男"), (2, "女"), (0, "未知")), verbose_name="性别", default=0)
    stuid = models.CharField(max_length=20, verbose_name="学号", blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "QQ个人信息"
        verbose_name_plural = verbose_name
