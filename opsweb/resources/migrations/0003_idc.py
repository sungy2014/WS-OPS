# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-07 13:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0002_auto_20171007_1759'),
    ]

    operations = [
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, unique=True, verbose_name='IDC 简称')),
                ('cn_name', models.CharField(max_length=100, verbose_name='IDC 中文名')),
                ('address', models.CharField(max_length=100, verbose_name='IDC 地址')),
                ('phone', models.CharField(max_length=20, null=True, verbose_name='IDC 联系电话')),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='IDC 邮箱')),
                ('user', models.CharField(max_length=32, null=True, verbose_name='IDC 联系人')),
            ],
            options={
                'db_table': 'idc',
            },
        ),
    ]
