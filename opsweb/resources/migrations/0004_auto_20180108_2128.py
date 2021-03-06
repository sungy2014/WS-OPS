# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-08 13:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0003_servermodel_zone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servermodel',
            name='monitor_status',
        ),
        migrations.AddField(
            model_name='servermodel',
            name='idrac_ip',
            field=models.GenericIPAddressField(null=True, protocol='IPv4', verbose_name='远程管理卡IP，适用于IDC服务器'),
        ),
        migrations.AlterField(
            model_name='servermodel',
            name='expired_time',
            field=models.DateTimeField(null=True, verbose_name='服务器过期/保时间'),
        ),
    ]
