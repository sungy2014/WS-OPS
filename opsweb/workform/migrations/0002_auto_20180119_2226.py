# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-19 14:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workform', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='processmodel',
            options={'ordering': ['step_id'], 'verbose_name': '工单流程表'},
        ),
        migrations.RenameField(
            model_name='processmodel',
            old_name='setp_id',
            new_name='step_id',
        ),
    ]