# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-14 11:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0006_auto_20180121_0016'),
    ]

    operations = [
        migrations.AddField(
            model_name='cmdbmodel',
            name='ansible_playbook',
            field=models.CharField(max_length=200, null=True, verbose_name='应用发布脚本'),
        ),
    ]
