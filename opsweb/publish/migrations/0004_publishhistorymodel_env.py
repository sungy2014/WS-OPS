# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-11 23:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publish', '0003_auto_20180311_2258'),
    ]

    operations = [
        migrations.AddField(
            model_name='publishhistorymodel',
            name='env',
            field=models.CharField(choices=[('online', '线上'), ('gray', '预发布')], max_length=10, null=True, verbose_name='环境'),
        ),
    ]
