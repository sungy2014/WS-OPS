# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-07 07:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='haha', max_length=20, verbose_name='用户名')),
            ],
        ),
    ]