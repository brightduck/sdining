# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-08 11:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0006_business_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='position',
            field=models.IntegerField(choices=[(1, '楚原食堂'), (2, '汉源食堂')], verbose_name='位置'),
        ),
    ]