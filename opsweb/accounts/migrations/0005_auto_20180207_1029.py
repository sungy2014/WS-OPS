# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-07 02:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20180130_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userextend',
            name='role',
            field=models.CharField(choices=[('0', 'Head'), ('1', 'Controller'), ('2', 'Manager'), ('3', 'Employee')], default='3', max_length=10, verbose_name='角色'),
        ),
    ]
