# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-20 16:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0005_auto_20180110_2142'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cmdbmodel',
            options={'ordering': ['-id'], 'verbose_name': 'CMDB表'},
        ),
        migrations.AlterModelOptions(
            name='cmdbstatisticbydaymodel',
            options={'ordering': ['myday'], 'verbose_name': 'CMDB按天统计表'},
        ),
        migrations.AlterModelOptions(
            name='idc',
            options={'permissions': (('view_idc', '查看idc列表'),), 'verbose_name': '机房表'},
        ),
        migrations.AlterModelOptions(
            name='servermodel',
            options={'ordering': ['-id'], 'verbose_name': '服务器表'},
        ),
        migrations.AlterModelOptions(
            name='serverstatisticbydaymodel',
            options={'ordering': ['myday'], 'verbose_name': '服务器按天统计表'},
        ),
    ]
