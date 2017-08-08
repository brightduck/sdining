from django.db import models

from storage.storage import ImgStorage


class Banner(models.Model):
    image = models.ImageField(upload_to='banner/%Y/%m', storage=ImgStorage(), verbose_name="幻灯片图")
    alttext = models.CharField(max_length=20, blank=True, verbose_name="img标签alt字段", help_text="当图片加载不出显示这个")
    url = models.URLField(blank=True, verbose_name="跳转地址")

    def __str__(self):
        return str(self.image)

    class Meta:
        verbose_name = "首页幻灯片"
        verbose_name_plural = verbose_name
