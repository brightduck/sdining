from django.db import models
from django.core.exceptions import ValidationError

from storage.storage import ImgStorage
from account.models import User


class Business(models.Model):
    user = models.OneToOneField(User, verbose_name="账号")
    name = models.CharField(max_length=50, verbose_name="商家名称")
    position = models.IntegerField(choices=((1, "楚园食堂"), (2, "汉园食堂")), verbose_name="位置", db_index=True)
    floor = models.IntegerField(choices=((1, "一楼"), (2, "二楼")), verbose_name="楼层")
    type = models.IntegerField(choices=((1, "餐品"), (2, "饮品")), verbose_name="商家类型", db_index=True)
    image = models.ImageField(upload_to='bimg/%Y/%m/%d', storage=ImgStorage(), blank=True, verbose_name="商家图片")
    average = models.IntegerField(default=10, verbose_name="人均消费")
    num_like = models.IntegerField(default=0, verbose_name="点赞数")
    rank = models.IntegerField(default=0, verbose_name="综合评价")

    is_open = models.BooleanField(default=False, verbose_name="是否接受预约")

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.is_open:
            for item in self.foodlist.all():
                item.can_reserve = False
                item.save()
        elif self.is_open:
            for item in self.foodlist.all():
                item.can_reserve = True
                item.save()
        super(Business, self).save()

    def delete(self, using=None, keep_parents=False):
        self.image.delete()
        super(Business, self).save()

    def get_pending_order_list(self):
        pass

    def get_food_list(self):
        return self.foodlist.all()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "商家"
        verbose_name_plural = verbose_name


class Food(models.Model):
    business = models.ForeignKey(Business, related_name='foodlist', verbose_name="商家")
    name = models.CharField(max_length=20, verbose_name="商品名")
    image = models.ImageField(upload_to='fimg/%Y/%m/%d', storage=ImgStorage(), blank=True, null=True,
                              verbose_name="商品图片")
    price = models.IntegerField(verbose_name="价格")
    can_reserve = models.BooleanField(default=False, verbose_name="可否预约")

    def clean(self):
        if self.can_reserve:
            if not self.business.is_open:
                raise ValidationError({'can_reserve': "此食物所属商家目前不接受预约"})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "食物"
        verbose_name_plural = verbose_name


class Special(models.Model):
    business = models.OneToOneField(Business, verbose_name="商家", related_name='special')
    foods = models.ManyToManyField(Food, verbose_name="食物")

    def __str__(self):
        return self.business.name

    class Meta:
        verbose_name = "特色菜"
        verbose_name_plural = verbose_name


class Authapply(models.Model):
    '''
    For Business Auth Apply
    '''
    user = models.OneToOneField(User, verbose_name="申请者")
    name = models.CharField(max_length=100, verbose_name="商家名称")
    position = models.IntegerField(choices=((1, "楚园食堂"), (2, "汉园食堂")), verbose_name="位置")
    floor = models.IntegerField(choices=((1, "一楼"), (2, "二楼")), verbose_name="楼层")
    type = models.IntegerField(choices=((1, "餐品"), (2, "饮品")), verbose_name="商家类型")
    date_apply = models.DateTimeField(auto_now_add=True, verbose_name="申请时间")

    is_passed = models.BooleanField(default=False, verbose_name="是否通过")

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.is_passed:
            self.user.is_active = True
            self.user.save()
            try:
                Business.objects.create(user=self.user, name=self.name, position=self.position,
                                        floor=self.floor,
                                        type=self.type)
            except:
                pass
        super(Authapply, self).save()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "商家认证申请"
        verbose_name_plural = verbose_name
