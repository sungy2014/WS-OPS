# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-28 08:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workform', '0023_workformmodel_reason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workformmodel',
            name='reason',
            field=models.CharField(choices=[('0', '项目需求'), ('1', '故障修复'), ('2', '技术优化'), ('3', '其他')], max_length=10, null=True, verbose_name='上线原因'),
        ),
    ]