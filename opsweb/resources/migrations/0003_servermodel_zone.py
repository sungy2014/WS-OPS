# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-07 08:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0002_auto_20180102_0003'),
    ]

    operations = [
        migrations.AddField(
            model_name='servermodel',
            name='zone',
            field=models.CharField(max_length=50, null=True, verbose_name='可用区'),
        ),
    ]
