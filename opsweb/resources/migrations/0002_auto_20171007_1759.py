# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-07 09:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server_idc',
            name='cpu_count',
            field=models.DecimalField(decimal_places=0, max_digits=3, null=True, verbose_name='CPU核数'),
        ),
        migrations.AlterField(
            model_name='server_idc',
            name='private_ip',
            field=models.GenericIPAddressField(protocol='IPv4', unique=True, verbose_name='私网IP'),
        ),
        migrations.AlterField(
            model_name='server_idc',
            name='public_ip',
            field=models.GenericIPAddressField(null=True, protocol='IPv4', verbose_name='公网IP'),
        ),
        migrations.AlterField(
            model_name='server_idc',
            name='status',
            field=models.DecimalField(decimal_places=0, max_digits=1, verbose_name='服务器状态:0-在线,1-下线'),
        ),
    ]