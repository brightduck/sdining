from django.db import models
from django.utils import timezone

from account.models import User
from business.models import Food


class Order(models.Model):
    user = models.ForeignKey(User, related_name='myorder', verbose_name="订单发起者")
    food = models.ForeignKey(Food, verbose_name="订单食物")
    comment = models.IntegerField(choices=((1, "挺好"), (2, "一般"), (3, "糟糕")), default=2, verbose_name="订单评价")
    date_create = models.DateTimeField(blank=True, null=True, verbose_name="创建时间")
    date_done = models.DateTimeField(blank=True, null=True, verbose_name="完成时间")

    is_accept = models.BooleanField(default=False, verbose_name="订单是否接受")
    is_done = models.BooleanField(default=False, verbose_name='订单是否完成')
    is_abnormal = models.BooleanField(default=False, verbose_name="订单是否是异常订单")

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.is_accept:
            self.date_create = timezone.now()
        if self.is_done:
            self.date_done = timezone.now()
        if self.is_abnormal:
            self.abnormalorder.order = self
            self.abnormalorder.save()
        super(Order, self).save()

    def get_business_user(self):
        return self.food.business.user

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "订单"
        verbose_name_plural = verbose_name


class AbnormalOrder(models.Model):
    order = models.OneToOneField(Order, verbose_name="订单")
    date_add = models.DateTimeField(default=timezone.now, verbose_name="加入时间")
    date_solve = models.DateTimeField(blank=True, null=True, verbose_name="解决时间")

    is_solve = models.BooleanField(default=False, verbose_name='是否解决')

    def get_order_user_object(self):
        return self.order.user

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.is_solve:
            self.date_solve = timezone.now()
        super(AbnormalOrder, self).save()

    def __str__(self):
        return self.order.date_create

    class Meta:
        verbose_name = "异常订单"
        verbose_name_plural = verbose_name
